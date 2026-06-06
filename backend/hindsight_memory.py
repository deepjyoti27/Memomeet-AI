import uuid
import json
from typing import List, Dict, Any
from backend.database import get_db_connection
from backend.groq_client import (
    extract_meeting_insights,
    detect_contradictions_with_history,
    generate_risk_predictions
)

def process_and_retain_meeting(
    meeting_id: str,
    title: str,
    customer_id: str,
    meeting_date: str,
    duration_seconds: int,
    transcript_lines: List[Dict[str, Any]],
    workspace_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Implements the 'Retain' phase of Hindsight Memory:
    1. Experience Network: Store raw transcript lines.
    2. World/Summary Network: Store meeting and customer profiles.
    3. Belief/Commitment Network: Extract and store decisions, requirements, etc.
    4. Reflect: Run cross-meeting contradiction scans and update risks.
    """
    # 1. Prepare raw transcript string
    from typing import Optional
    full_transcript_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in transcript_lines])
    
    # 2. Extract structured insights via Groq Client / Local Simulator
    insights = extract_meeting_insights(title, full_transcript_text)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if customer exists, if not create a default one
    cursor.execute("SELECT id FROM customers WHERE id = ?", (customer_id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO customers (id, name, industry, workspace_id) VALUES (?, ?, ?, ?)",
            (customer_id, customer_id.replace("-", " ").title(), "Technology", workspace_id)
        )
    else:
        if workspace_id:
            cursor.execute("UPDATE customers SET workspace_id = ? WHERE id = ? AND (workspace_id IS NULL OR workspace_id = '')", (workspace_id, customer_id))
    
    # 3. Store Meeting Record
    cursor.execute(
        """
        INSERT INTO meetings (
            id, title, customer_id, workspace_id, meeting_date, duration_seconds, iq_score, iq_breakdown, sentiment_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            meeting_id,
            title,
            customer_id,
            workspace_id,
            meeting_date,
            duration_seconds,
            insights.get("iq_score", 80),
            json.dumps(insights.get("iq_breakdown", {})),
            insights.get("sentiment_score", 0.0)
        )
    )
    
    # 4. Store Transcript lines (Experience Network)
    for line in transcript_lines:
        line_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO transcripts (id, meeting_id, speaker, start_time, end_time, text) VALUES (?, ?, ?, ?, ?, ?)",
            (
                line_id,
                meeting_id,
                line.get("speaker"),
                line.get("start_time", 0.0),
                line.get("end_time", 0.0),
                line.get("text")
            )
        )
        
    # Retrieve existing historical memory nodes for contradiction checks BEFORE inserting new ones
    cursor.execute(
        "SELECT id, meeting_id, category, content, speaker FROM memory_nodes WHERE customer_id = ?",
        (customer_id,)
    )
    history_rows = cursor.fetchall()
    history_nodes = [dict(row) for row in history_rows]
    
    # 5. Store new Belief/Commitment nodes
    new_nodes_to_insert = []
    categories = ["decisions", "requirements", "deadlines", "risks", "commitments", "action_items", "objections"]
    
    category_map = {
        "decisions": "decision",
        "requirements": "requirement",
        "deadlines": "deadline",
        "risks": "risk",
        "commitments": "commitment",
        "action_items": "action_item",
        "objections": "objection"
    }
    
    for cat_plural in categories:
        cat_single = category_map[cat_plural]
        for node in insights.get(cat_plural, []):
            node_id = str(uuid.uuid4())
            content = node.get("content")
            speaker = node.get("speaker", "Unknown")
            confidence = node.get("confidence", 0.8)
            
            # Find a context excerpt from the transcript
            context_text = find_context_excerpt(content, transcript_lines)
            
            new_nodes_to_insert.append({
                "id": node_id,
                "meeting_id": meeting_id,
                "customer_id": customer_id,
                "category": cat_single,
                "content": content,
                "context_text": context_text,
                "speaker": speaker,
                "confidence_level": confidence
            })
            
            # Insert into SQLite
            cursor.execute(
                """
                INSERT INTO memory_nodes (
                    id, meeting_id, customer_id, category, content, context_text, speaker, confidence_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (node_id, meeting_id, customer_id, cat_single, content, context_text, speaker, confidence)
            )
            
            # Build initial relationship edges
            # Link Customer to node
            edge_id1 = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO memory_edges (id, source_id, target_id, relation_type) VALUES (?, ?, ?, ?)",
                (edge_id1, customer_id, node_id, f"HAS_{cat_single.upper()}")
            )
            
            # Link Meeting to node
            edge_id2 = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO memory_edges (id, source_id, target_id, relation_type) VALUES (?, ?, ?, ?)",
                (edge_id2, meeting_id, node_id, f"CONTAINS_{cat_single.upper()}")
            )
            
    # 6. Reflect Phase: Detect Contradictions
    if history_nodes:
        detected_contradictions = detect_contradictions_with_history(new_nodes_to_insert, history_nodes)
        for contra in detected_contradictions:
            contra_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO contradictions (
                    id, customer_id, meeting_id_a, meeting_id_b, node_id_a, node_id_b,
                    statement_a, statement_b, explanation, severity, resolved
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    contra_id,
                    customer_id,
                    contra["meeting_id_a"],
                    contra["meeting_id_b"],
                    contra["node_id_a"],
                    contra["node_id_b"],
                    contra["statement_a"],
                    contra["statement_b"],
                    contra["explanation"],
                    contra["severity"]
                )
            )
            
    # 7. Update Risk Predictions
    # Get all customer nodes (including new ones) to run risk engine
    cursor.execute(
        "SELECT id, category, content, speaker FROM memory_nodes WHERE customer_id = ?",
        (customer_id,)
    )
    all_customer_rows = cursor.fetchall()
    all_customer_nodes = [dict(row) for row in all_customer_rows]
    
    # Delete old risks for this customer to replace with fresh ones
    cursor.execute("DELETE FROM risks WHERE customer_id = ?", (customer_id,))
    
    predicted_risks = generate_risk_predictions(customer_id, all_customer_nodes)
    for risk in predicted_risks:
        risk_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO risks (
                id, customer_id, meeting_id, category, risk_level, probability, impact, evidence, mitigation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                risk_id,
                customer_id,
                meeting_id,
                risk["category"],
                risk["risk_level"],
                risk["probability"],
                risk["impact"],
                json.dumps(risk["evidence"]),
                risk["mitigation"]
            )
        )
        
    conn.commit()
    conn.close()
    
    return insights

def find_context_excerpt(content: str, transcript_lines: List[Dict[str, Any]]) -> str:
    """Finds a matching transcript sentence/dialogue surrounding a keyword in content."""
    keywords = [w for w in content.split() if len(w) > 4]
    if not keywords:
        return ""
        
    for line in transcript_lines:
        text = line.get("text", "")
        # If the content matches a large chunk or multiple keywords
        if any(kw.lower() in text.lower() for kw in keywords[:3]):
            return f"{line.get('speaker')}: \"{text}\""
            
    # Fallback
    if transcript_lines:
        return f"{transcript_lines[0].get('speaker')}: \"{transcript_lines[0].get('text')}\""
    return ""
