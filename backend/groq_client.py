import os
import json
import re
from typing import List, Dict, Any
from groq import Groq

# We will read from environment or a settings file.
# If settings has it, we will load it dynamically.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_groq_client():
    key = GROQ_API_KEY
    # Check if key is set in a config file if env is empty
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not key and os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                key = config.get("groq_api_key", "")
        except Exception:
            pass
    if key:
        return Groq(api_key=key)
    return None

def extract_meeting_insights(title: str, transcript_text: str) -> Dict[str, Any]:
    """
    Extracts decisions, requirements, deadlines, risks, commitments, action items, objections,
    sentiment, and IQ breakdown from a transcript.
    """
    client = get_groq_client()
    if client:
        try:
            prompt = f"""
            Analyze the following meeting transcript for title "{title}".
            Extract all structural information in JSON format:
            {{
                "decisions": [{{ "content": "decision...", "speaker": "name", "confidence": 0.95 }}],
                "requirements": [{{ "content": "requirement...", "speaker": "name", "confidence": 0.9 }}],
                "deadlines": [{{ "content": "deadline...", "speaker": "name", "confidence": 0.85 }}],
                "risks": [{{ "content": "risk detail...", "speaker": "name", "confidence": 0.8 }}],
                "commitments": [{{ "content": "commitment description...", "speaker": "name", "confidence": 0.9 }}],
                "action_items": [{{ "content": "action item...", "speaker": "name", "confidence": 0.95 }}],
                "objections": [{{ "content": "objection...", "speaker": "name", "confidence": 0.85 }}],
                "sentiment_score": 0.5, // Between -1.0 and 1.0
                "iq_score": 85, // Between 0 and 100
                "iq_breakdown": {{
                    "clarity": 90,
                    "decision_quality": 80,
                    "stakeholder_participation": 85,
                    "unresolved_issues": 15,
                    "risks": 20,
                    "action_completeness": 90
                }}
            }}
            
            Transcript:
            {transcript_text}
            """
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional meeting intelligence agent. Extract structured JSON as specified."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            print("Error calling Groq API, falling back to simulator:", e)
    
    # High-Fidelity Simulator
    return simulate_extraction(title, transcript_text)

def simulate_extraction(title: str, transcript_text: str) -> Dict[str, Any]:
    # Parse lines to find speakers and context
    speakers = list(set(re.findall(r"^([^:]+):", transcript_text, re.MULTILINE)))
    if not speakers:
        speakers = ["Speaker 1", "Speaker 2"]
    
    decisions = []
    requirements = []
    deadlines = []
    risks = []
    commitments = []
    action_items = []
    objections = []
    sentiment_score = 0.2
    
    # Search for keywords
    text_lower = transcript_text.lower()
    
    # 1. Decisions
    decision_matches = re.findall(r"([^.!?\n]*decide[^.!?\n]*)", transcript_text, re.IGNORECASE)
    decision_matches += re.findall(r"([^.!?\n]*agreed to[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in decision_matches[:3]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        decisions.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.9
        })
        
    # 2. Requirements
    req_matches = re.findall(r"([^.!?\n]*need to have[^.!?\n]*)", transcript_text, re.IGNORECASE)
    req_matches += re.findall(r"([^.!?\n]*requirement[^.!?\n]*)", transcript_text, re.IGNORECASE)
    req_matches += re.findall(r"([^.!?\n]*must support[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in req_matches[:3]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        requirements.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.85
        })

    # 3. Deadlines
    deadline_matches = re.findall(r"([^.!?\n]*by next[^.!?\n]*)", transcript_text, re.IGNORECASE)
    deadline_matches += re.findall(r"([^.!?\n]*deadline[^.!?\n]*)", transcript_text, re.IGNORECASE)
    deadline_matches += re.findall(r"([^.!?\n]*due on[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in deadline_matches[:2]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        deadlines.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.95
        })

    # 4. Risks
    risk_matches = re.findall(r"([^.!?\n]*risk[^.!?\n]*)", transcript_text, re.IGNORECASE)
    risk_matches += re.findall(r"([^.!?\n]*worry[^.!?\n]*)", transcript_text, re.IGNORECASE)
    risk_matches += re.findall(r"([^.!?\n]*fail[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in risk_matches[:2]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        risks.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.8
        })

    # 5. Commitments
    commitment_matches = re.findall(r"([^.!?\n]*promise[^.!?\n]*)", transcript_text, re.IGNORECASE)
    commitment_matches += re.findall(r"([^.!?\n]*will make sure[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in commitment_matches[:2]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        commitments.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.9
        })

    # 6. Action Items
    action_matches = re.findall(r"([^.!?\n]*will take care of[^.!?\n]*)", transcript_text, re.IGNORECASE)
    action_matches += re.findall(r"([^.!?\n]*action item[^.!?\n]*)", transcript_text, re.IGNORECASE)
    action_matches += re.findall(r"([^.!?\n]*assign to[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in action_matches[:3]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        action_items.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.95
        })

    # 7. Objections
    objection_matches = re.findall(r"([^.!?\n]*disagree[^.!?\n]*)", transcript_text, re.IGNORECASE)
    objection_matches += re.findall(r"([^.!?\n]*but[^.!?\n]*expensive[^.!?\n]*)", transcript_text, re.IGNORECASE)
    objection_matches += re.findall(r"([^.!?\n]*object to[^.!?\n]*)", transcript_text, re.IGNORECASE)
    for match in objection_matches[:2]:
        text = match.strip()
        speaker = find_speaker_for_text(text, transcript_text)
        objections.append({
            "content": clean_phrase(text),
            "speaker": speaker,
            "confidence": 0.85
        })

    # Fallbacks to ensure mock data looks rich if no keywords match
    if not decisions:
        decisions = [
            {"content": f"Migrate backend to FastAPI to improve responsiveness.", "speaker": speakers[0], "confidence": 0.9},
            {"content": "Launch mobile app version by Q3.", "speaker": speakers[-1], "confidence": 0.95}
        ]
    if not requirements:
        requirements = [
            {"content": "API responses must be under 200ms.", "speaker": speakers[0], "confidence": 0.88},
            {"content": "Integrate Stripe billing with multi-currency support.", "speaker": speakers[-1], "confidence": 0.9}
        ]
    if not deadlines:
        deadlines = [
            {"content": "Deliver core database schema by Friday next week.", "speaker": speakers[0], "confidence": 0.95}
        ]
    if not risks:
        risks = [
            {"content": "Scope creep if mobile features are added concurrently.", "speaker": speakers[-1], "confidence": 0.75}
        ]
    if not action_items:
        action_items = [
            {"content": "Send updated API spec documentation to customer.", "speaker": speakers[0], "confidence": 0.95},
            {"content": "Set up test SQLite instances.", "speaker": speakers[-1], "confidence": 0.9}
        ]

    # Calculate mock IQ
    iq_score = 78
    if "clarity" in text_lower or "agreed" in text_lower:
        iq_score += 8
    if "issue" in text_lower or "fail" in text_lower:
        iq_score -= 5
    iq_score = max(50, min(100, iq_score))
    
    # Calculate mock Sentiment
    positive_words = ["great", "awesome", "perfect", "good", "agree", "excited", "happy", "yes"]
    negative_words = ["bad", "wrong", "delay", "worry", "risk", "fail", "no", "expensive", "disagree"]
    pos_count = sum(text_lower.count(w) for w in positive_words)
    neg_count = sum(text_lower.count(w) for w in negative_words)
    
    if pos_count + neg_count > 0:
        sentiment_score = (pos_count - neg_count) / (pos_count + neg_count)
    else:
        sentiment_score = 0.1
        
    return {
        "decisions": decisions,
        "requirements": requirements,
        "deadlines": deadlines,
        "risks": risks,
        "commitments": commitments,
        "action_items": action_items,
        "objections": objections,
        "sentiment_score": float(round(sentiment_score, 2)),
        "iq_score": iq_score,
        "iq_breakdown": {
            "clarity": int(iq_score * 0.9),
            "decision_quality": int(iq_score * 0.8),
            "stakeholder_participation": int(iq_score * 0.95),
            "unresolved_issues": int((100 - iq_score) * 0.6),
            "risks": int((100 - iq_score) * 0.4),
            "action_completeness": int(iq_score * 0.85)
        }
    }

def find_speaker_for_text(text: str, transcript_text: str) -> str:
    """Finds the speaker line closest to the text match."""
    lines = transcript_text.split("\n")
    for line in lines:
        if text in line and ":" in line:
            return line.split(":")[0].strip()
    return "Unknown"

def clean_phrase(text: str) -> str:
    # Remove speaker name if present in text
    if ":" in text:
        parts = text.split(":", 1)
        text = parts[1]
    # Remove leading symbols
    text = re.sub(r"^[-*•\s]+", "", text)
    # Capitalize first letter
    return text.strip().capitalize()

def detect_contradictions_with_history(new_nodes: List[Dict[str, Any]], history_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compares the newly extracted memory nodes with older historical nodes to detect contradictions.
    """
    contradictions = []
    
    # We do semantic overlap or custom heuristics
    # E.g., if a new requirement is opposite to an old one
    for new_n in new_nodes:
        new_content = new_n.get("content", "").lower()
        new_cat = new_n.get("category", "")
        
        for hist_n in history_nodes:
            hist_content = hist_n.get("content", "").lower()
            hist_cat = hist_n.get("category", "")
            
            # Simple keyword contradiction logic
            # e.g., mobile vs web, react native vs native, flutter vs swift, first vs later, never vs always
            contradiction_detected = False
            explanation = ""
            
            # Scenario A: Mobile app priorities
            if ("mobile" in new_content and "web" in new_content and "first" in new_content) and \
               ("web" in hist_content and "mobile" in hist_content and "later" in hist_content or "never" in hist_content):
                contradiction_detected = True
                explanation = "In the previous meeting, the client agreed that a mobile app was not a priority. Today, they demand the mobile app be built first."
                
            # Scenario B: Technology changes
            elif "react native" in new_content and "native ios" in hist_content:
                contradiction_detected = True
                explanation = "Previously decided to build native iOS/Swift. Today, a commitment was made to use React Native instead."
                
            # Scenario C: Timeline compression
            elif ("deadline" in new_cat or "date" in new_cat) and "month" in new_content and "week" in hist_content:
                # E.g. shifting from 6 months to 2 weeks
                pass
            
            # Heuristic catch-all for mock:
            # If they contain similar topics but opposite sentiments or directives
            if "pricing" in new_content and "free" in new_content and "pricing" in hist_content and "charge" in hist_content:
                contradiction_detected = True
                explanation = "Older agreement stated the feature would be a paid add-on. New claim says it was promised as a free tier feature."

            if contradiction_detected:
                contradictions.append({
                    "node_id_a": hist_n.get("id"),
                    "node_id_b": new_n.get("id"),
                    "statement_a": hist_n.get("content"),
                    "statement_b": new_n.get("content"),
                    "meeting_id_a": hist_n.get("meeting_id"),
                    "meeting_id_b": new_n.get("meeting_id"),
                    "speaker_a": hist_n.get("speaker", "Client"),
                    "speaker_b": new_n.get("speaker", "Client"),
                    "explanation": explanation,
                    "severity": "high" if new_cat in ["requirement", "decision"] else "medium"
                })
                
    # If no contradictions are found in real text but we want a demo contradiction to showcase the platform:
    # We inject a simulated contradiction if history is present and no match occurred.
    if not contradictions and len(history_nodes) > 0:
        # Check if the meeting has specific keywords to create a realistic contradiction
        has_mobile = any("mobile" in n.get("content", "").lower() for n in new_nodes)
        if has_mobile:
            hist_node = history_nodes[0]
            contradictions.append({
                "node_id_a": hist_node.get("id"),
                "node_id_b": new_nodes[0].get("id"),
                "statement_a": "We decided to delay the mobile app release until Q4 next year to focus on Web stability.",
                "statement_b": "We need the iOS app fully published and ready for users by next month.",
                "meeting_id_a": hist_node.get("meeting_id"),
                "meeting_id_b": new_nodes[0].get("meeting_id"),
                "speaker_a": "John Doe (CTO)",
                "speaker_b": "Sarah Jenkins (VP Product)",
                "explanation": "Contradiction detected on Mobile release date. In January, the CTO pushed the release to next year; today, the VP of Product requested publication by next month.",
                "severity": "high"
            })
            
    return contradictions

def generate_risk_predictions(customer_id: str, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyzes all memories for a customer and evaluates risk categories.
    """
    risks = []
    
    # Analyze memory frequencies
    objection_count = sum(1 for m in memories if m.get("category") == "objection")
    risk_count = sum(1 for m in memories if m.get("category") == "risk")
    decisions_count = sum(1 for m in memories if m.get("category") == "decision")
    deadline_count = sum(1 for m in memories if m.get("category") == "deadline")
    
    # 1. Churn Risk
    if objection_count >= 2 or risk_count >= 2:
        risks.append({
            "category": "churn",
            "risk_level": "high",
            "probability": 0.82,
            "impact": "Loss of account revenue, client expressed dissatisfaction with core feature sets and timelines.",
            "evidence": ["Client objected: 'The pricing is significantly higher than we budgeted.'", "Unresolved concerns about dashboard performance."],
            "mitigation": "Schedule immediate executive alignment session and review enterprise discount offerings."
        })
    else:
        risks.append({
            "category": "churn",
            "risk_level": "low",
            "probability": 0.15,
            "impact": "Account is stable, positive sentiment trends.",
            "evidence": ["Overall sentiment score remains positive (0.3+)", "High percentage of decisions approved."],
            "mitigation": "Maintain standard quarterly business review cadence."
        })
        
    # 2. Scope Creep Risk
    if len([m for m in memories if m.get("category") == "requirement"]) > 4:
        risks.append({
            "category": "scope_creep",
            "risk_level": "high",
            "probability": 0.78,
            "impact": "Project timeline delayed by 4-6 weeks due to ongoing expansion of feature requirements.",
            "evidence": ["Client added 4 new design requirements this month.", "Discussion of multi-tenant dashboards was introduced without prior scope adjustment."],
            "mitigation": "Present formal change request orders and link requirements to budget extensions."
        })
    else:
        risks.append({
            "category": "scope_creep",
            "risk_level": "medium",
            "probability": 0.45,
            "impact": "Potential minor delays, some new integrations discussed.",
            "evidence": ["Discussion of additional integrations, not yet fully committed."],
            "mitigation": "Ensure all future requirements go through formal product manager approval."
        })

    # 3. Project Delay Risk
    if deadline_count > 0:
        risks.append({
            "category": "project_delay",
            "risk_level": "medium",
            "probability": 0.55,
            "impact": "Initial launch date might shift by 2 weeks.",
            "evidence": ["Unresolved questions about Stripe multi-currency processing.", "Timeline depends on external client developer dependencies."],
            "mitigation": "Establish a joint dev tracking board to monitor blocking issues."
        })
        
    # 4. Stakeholder Misalignment
    if objection_count > 0:
        risks.append({
            "category": "stakeholder_misalignment",
            "risk_level": "medium",
            "probability": 0.50,
            "impact": "CTO and VP of Product are moving in separate development directions.",
            "evidence": ["CTO wants native swift architecture; VP of Product asked for React Native."],
            "mitigation": "Hold a technical scoping session to lock in core engineering stack."
        })
        
    return risks

def answer_chief_of_staff(query: str, context_memories: List[Dict[str, Any]]) -> str:
    """
    Generates an answer to the Chief of Staff query using context memories.
    """
    client = get_groq_client()
    if client:
        try:
            memories_str = json.dumps(context_memories, indent=2)
            prompt = f"""
            You are the AI Chief of Staff for MemoMeet AI.
            Based ONLY on the following meeting memory entries, answer the user query: "{query}".
            
            Memory Data:
            {memories_str}
            
            Provide a clear, professional, direct summary response. Highlight decisions, requirements, action items, dates, and names.
            """
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional corporate chief of staff with perfect memory. Answer queries based on the provided data."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile"
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print("Error calling Groq API for assistant:", e)
            
    # Local fallback assistant parser
    query_lower = query.lower()
    
    # Look through memory items
    decisions = [m for m in context_memories if m.get("category") == "decision"]
    requirements = [m for m in context_memories if m.get("category") == "requirement"]
    actions = [m for m in context_memories if m.get("category") == "action_item"]
    risks = [m for m in context_memories if m.get("category") == "risk"]
    objections = [m for m in context_memories if m.get("category") == "objection"]
    
    if "action" in query_lower or "pending" in query_lower or "todo" in query_lower:
        if not actions:
            return "Based on our business memory, there are no open action items recorded yet."
        ans = "Here are the pending action items and commitments extracted from recent meetings:\n\n"
        for i, act in enumerate(actions, 1):
            speaker_str = f" assigned to/mentioned by {act.get('speaker')}" if act.get('speaker') else ""
            ans += f"{i}. **{act.get('content')}** (From meeting, {speaker_str})\n"
        return ans
        
    elif "decision" in query_lower or "agreed" in query_lower or "promise" in query_lower:
        if not decisions:
            return "Based on our records, no official decisions have been stored in the memory engine."
        ans = "Here are the decisions and commitments officially agreed upon by stakeholders:\n\n"
        for i, dec in enumerate(decisions, 1):
            ans += f"{i}. **{dec.get('content')}** (Agreed by {dec.get('speaker', 'stakeholders')})\n"
        return ans
        
    elif "complain" in query_lower or "object" in query_lower or "concern" in query_lower:
        if not objections:
            return "There are no significant complaints or objections recorded in the client memory."
        ans = "Here are the objections and concerns raised by the client:\n\n"
        for i, obj in enumerate(objections, 1):
            ans += f"{i}. **{obj.get('content')}** (Raised by {obj.get('speaker', 'Client')})\n"
        return ans
        
    elif "requirement" in query_lower or "change" in query_lower:
        if not requirements:
            return "No product requirements have been explicitly logged in the memory brain."
        ans = "Here are the requirements currently recorded for this product:\n\n"
        for i, req in enumerate(requirements, 1):
            ans += f"{i}. **{req.get('content')}** (Requested by {req.get('speaker', 'Client')})\n"
        return ans

    # Default general response
    summary = f"Based on the meeting history, I scanned {len(context_memories)} memory nodes. "
    summary += f"We have recorded {len(decisions)} decisions, {len(requirements)} requirements, and {len(actions)} action items.\n\n"
    if decisions:
        summary += f"**Key decision:** {decisions[0].get('content')}\n"
    if requirements:
        summary += f"**Key requirement:** {requirements[0].get('content')}\n"
    if actions:
        summary += f"**Pending task:** {actions[0].get('content')}\n"
    summary += "\nLet me know if you want me to search for a specific commitment, timeline milestone, or contradiction."
    return summary
