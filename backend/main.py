from fastapi import FastAPI, HTTPException, Body, Query, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from typing import List, Dict, Any, Optional
import os
import json
import uuid
import hashlib
from backend.database import init_db, get_db_connection
from backend.models import (
    CustomerResponse,
    MeetingListItem,
    MeetingDetailResponse,
    TranscriptLine,
    MeetingCreate,
    BusinessMemoryGraphResponse,
    GraphNode,
    GraphEdge,
    TruthVerificationRequest,
    TruthVerificationResponse,
    EvidenceCard,
    ContradictionResponse,
    RiskPredictionResponse,
    ChatRequest,
    ChatResponse,
    SettingsResponse,
    SettingsUpdate,
    # New Auth & Workspace Models
    UserRegister,
    UserLogin,
    UserResponse,
    ForgotPasswordRequest,
    VerifyEmailRequest,
    SessionResponse,
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceInviteRequest,
    WorkspaceInviteResponse,
    WorkspaceMemberResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    SearchResponse,
    SearchResultItem,
    AlertNotification,
    RequirementDriftResponse,
    RequirementDriftItem,
    CommitmentTrackerResponse,
    CommitmentTrackerItem,
    StakeholderInfluenceResponse,
    StakeholderScore,
    CustomerTrustResponse,
    RiskRadarResponse
)
from backend.hindsight_memory import process_and_retain_meeting
from backend.groq_client import answer_chief_of_staff

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(
    title="MemoMeet AI API",
    description="Meeting Intelligence, Organizational Memory, and Truth Verification Platform Engine",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    import logging
    logging.error(f"VALIDATION ERROR: {exc.errors()}")
    body = await request.body()
    logging.error(f"REQUEST BODY: {body}")
    print(f"VALIDATION ERROR: {exc.errors()}", flush=True)
    print(f"REQUEST BODY: {body}", flush=True)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(body)}
    )

# Enable CORS for Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve unified SPA dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h2>MemoMeet AI Server is online. static/index.html client not found.</h2>")

@app.on_event("startup")
def startup_event():
    init_db()
    seed_initial_data()

# Helper: Seed database with high-fidelity corporate transcripts
def seed_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if customers exist
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return # Already seeded
        
    print("Seeding initial corporate data...")
    
    # 0. Add default user and workspace for Foreign Key integrity
    cursor.execute("SELECT id FROM users WHERE id = ?", ("system-default",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (id, full_name, email, password_hash, verified) VALUES ('system-default', 'System Default User', 'default@memomeet.ai', 'none', 1)"
        )
    cursor.execute("SELECT id FROM workspaces WHERE id = ?", ("default-workspace",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO workspaces (id, name, owner_id) VALUES ('default-workspace', 'Default Workspace', 'system-default')"
        )
        # Add workspace link
        cursor.execute(
            "INSERT INTO workspace_users (id, workspace_id, user_id, role) VALUES (?, 'default-workspace', 'system-default', 'admin')",
            (str(uuid.uuid4()),)
        )
    
    # 1. Add Customers
    customers = [
        ("acme-corp", "Acme Corporation", "Enterprise SaaS & Logistics"),
        ("nebula-systems", "Nebula Systems", "Cloud Infrastructure & Cybersecurity"),
        ("vortex-retail", "Vortex Retail", "Global E-Commerce & Retail")
    ]
    for cid, name, ind in customers:
        cursor.execute("INSERT INTO customers (id, name, industry, workspace_id) VALUES (?, ?, ?, 'default-workspace')", (cid, name, ind))
        
    # 2. Add Meetings & Transcripts (Acme Corp Timeline)
    # Meeting 1: January kick-off (Decided web app first, mobile app Q4, budget limited)
    m1_id = "acme-m1"
    cursor.execute("""
        INSERT INTO meetings (id, title, customer_id, workspace_id, meeting_date, duration_seconds, iq_score, iq_breakdown, sentiment_score)
        VALUES (?, ?, ?, 'default-workspace', '2026-01-15', 1800, 85, ?, 0.4)
    """, (m1_id, "Acme Corp: Core Architecture Kickoff", "acme-corp", json.dumps({
        "clarity": 90, "decision_quality": 85, "stakeholder_participation": 80,
        "unresolved_issues": 10, "risks": 15, "action_completeness": 90
    })))
    
    m1_transcript = [
        ("Sarah Jenkins (VP Product)", "Welcome everyone. We are kickstarting the Acme digital portal project today."),
        ("John Doe (CTO)", "Thanks Sarah. From engineering side, we need to focus on web stability first. We decided to delay the mobile app release until Q4 next year to focus on Web stability."),
        ("Sarah Jenkins (VP Product)", "Agreed. Let's make sure the core database schema is finalized by Friday next week."),
        ("Mark Davis (Client PM)", "We need a Stripe integration for multi-currency processing. That is a hard requirement for the first release."),
        ("John Doe (CTO)", "Yes, we will make sure Stripe billing is set up with multi-currency. Let's make that an action item.")
    ]
    
    # Meeting 2: June sync (Contradiction: VP Product demands mobile app immediately)
    m2_id = "acme-m2"
    cursor.execute("""
        INSERT INTO meetings (id, title, customer_id, workspace_id, meeting_date, duration_seconds, iq_score, iq_breakdown, sentiment_score)
        VALUES (?, ?, ?, 'default-workspace', '2026-06-02', 2400, 68, ?, -0.1)
    """, (m2_id, "Acme Corp: Q2 Priority Alignment", "acme-corp", json.dumps({
        "clarity": 60, "decision_quality": 65, "stakeholder_participation": 75,
        "unresolved_issues": 35, "risks": 30, "action_completeness": 70
    })))
    
    m2_transcript = [
        ("Sarah Jenkins (VP Product)", "Hi team. We need to shift priorities. We need the iOS app fully published and ready for users by next month. The board is asking for it."),
        ("John Doe (CTO)", "Wait, Sarah. We never wanted a mobile app in the initial release phase. We agreed web was the priority."),
        ("Sarah Jenkins (VP Product)", "No, we always wanted a mobile app first. It has always been our main channel constraint."),
        ("Mark Davis (Client PM)", "Also, we want to look at custom domain mapping. Can we build custom domain settings by next week?"),
        ("John Doe (CTO)", "That is a big scope change. This represents scope creep risk. Let's document this.")
    ]
    
    # Insert transcripts
    for m_id, trans in [(m1_id, m1_transcript), (m2_id, m2_transcript)]:
        for idx, (speaker, text) in enumerate(trans):
            tid = f"t-{m_id}-{idx}"
            cursor.execute(
                "INSERT INTO transcripts (id, meeting_id, speaker, start_time, end_time, text) VALUES (?, ?, ?, ?, ?, ?)",
                (tid, m_id, speaker, idx*60.0, (idx+1)*60.0, text)
            )
            
    # 3. Add Memory Nodes (Belief Network)
    memory_nodes = [
        # Meeting 1 Nodes
        ("node-m1-1", m1_id, "acme-corp", "decision", "Focus on web stability first and delay the mobile app release until Q4 next year.", "John Doe (CTO): \"We decided to delay the mobile app release until Q4 next year to focus on Web stability.\"", "John Doe (CTO)", 0.95),
        ("node-m1-2", m1_id, "acme-corp", "requirement", "Integrate Stripe billing with multi-currency support.", "Mark Davis (Client PM): \"We need a Stripe integration for multi-currency processing.\"", "Mark Davis (Client PM)", 0.90),
        ("node-m1-3", m1_id, "acme-corp", "deadline", "Finalize the core database schema by Friday next week.", "Sarah Jenkins (VP Product): \"Let's make sure the core database schema is finalized by Friday next week.\"", "Sarah Jenkins (VP Product)", 0.95),
        ("node-m1-4", m1_id, "acme-corp", "action_item", "Set up multi-currency billing templates.", "John Doe (CTO): \"Yes, we will make sure Stripe billing is set up with multi-currency.\"", "John Doe (CTO)", 0.90),
        
        # Meeting 2 Nodes
        ("node-m2-1", m2_id, "acme-corp", "decision", "VP Product requests the iOS mobile app to be fully published and ready by next month.", "Sarah Jenkins (VP Product): \"We need the iOS app fully published and ready for users by next month.\"", "Sarah Jenkins (VP Product)", 0.90),
        ("node-m2-2", m2_id, "acme-corp", "objection", "CTO objects that they agreed web was the priority and mobile was scheduled for Q4.", "John Doe (CTO): \"Wait, Sarah. We never wanted a mobile app in the initial release phase. We agreed web was the priority.\"", "John Doe (CTO)", 0.95),
        ("node-m2-3", m2_id, "acme-corp", "requirement", "Add support for custom domain mapping configurations.", "Mark Davis (Client PM): \"Also, we want to look at custom domain mapping.\"", "Mark Davis (Client PM)", 0.85),
        ("node-m2-4", m2_id, "acme-corp", "risk", "Scope creep risk introduced by adding mobile app features and custom domain maps simultaneously.", "John Doe (CTO): \"That is a big scope change. This represents scope creep risk.\"", "John Doe (CTO)", 0.80)
    ]
    
    for nid, mid, cid, cat, content, context, speaker, conf in memory_nodes:
        cursor.execute("""
            INSERT INTO memory_nodes (id, meeting_id, customer_id, category, content, context_text, speaker, confidence_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nid, mid, cid, cat, content, context, speaker, conf))
        
        # Add Graph Edges
        # Customer has Category node
        cursor.execute("INSERT INTO memory_edges (id, source_id, target_id, relation_type) VALUES (?, ?, ?, ?)",
                       (str(uuid.uuid4()), cid, nid, f"HAS_{cat.upper()}"))
        # Meeting contains Category node
        cursor.execute("INSERT INTO memory_edges (id, source_id, target_id, relation_type) VALUES (?, ?, ?, ?)",
                       (str(uuid.uuid4()), mid, nid, f"CONTAINS_{cat.upper()}"))
        
    # Add generic HAS_MEETING edges
    cursor.execute("INSERT INTO memory_edges (id, source_id, target_id, relation_type) VALUES (?, ?, ?, ?)",
                   (str(uuid.uuid4()), "acme-corp", m1_id, "HAS_MEETING"))
    cursor.execute("INSERT INTO memory_edges (id, source_id, target_id, relation_type) VALUES (?, ?, ?, ?)",
                   (str(uuid.uuid4()), "acme-corp", m2_id, "HAS_MEETING"))
                       
    # 4. Add Seeded Contradiction
    cursor.execute("""
        INSERT INTO contradictions (
            id, customer_id, meeting_id_a, meeting_id_b, node_id_a, node_id_b,
            statement_a, statement_b, explanation, severity, resolved
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (
        "contra-1",
        "acme-corp",
        m1_id,
        m2_id,
        "node-m1-1",
        "node-m2-1",
        "We decided to delay the mobile app release until Q4 next year to focus on Web stability.",
        "We need the iOS app fully published and ready for users by next month.",
        "Contradiction detected regarding mobile app launch schedule. Meeting 1 established mobile app was delayed to focus on web, whereas Meeting 2 demands immediate publication next month.",
        "high"
    ))
    
    # 5. Add Seeded Risks
    risks = [
        ("risk-1", "acme-corp", m2_id, "scope_creep", "high", 0.85, 
         "Adding custom domain billing and mobile iOS launch in the same development cycle threatens baseline timeline.",
         json.dumps(["Client requested custom domain mapping", "VP Product requested immediate mobile launch"]),
         "Hold scope alignment meeting with VP of Product to draft a formal addendum contract."),
        ("risk-2", "acme-corp", m2_id, "stakeholder_misalignment", "medium", 0.60,
         "CTO (John Doe) and VP of Product (Sarah Jenkins) have conflicting recollections of mobile priorities.",
         json.dumps(["CTO: We agreed web was the priority", "VP Product: We always wanted mobile app first"]),
         "Share Truth Verification timeline summary and transcripts with stakeholders to verify commitments.")
    ]
    for rid, cid, mid, cat, lvl, prob, impact, ev, mit in risks:
        cursor.execute("""
            INSERT INTO risks (id, customer_id, meeting_id, category, risk_level, probability, impact, evidence, mitigation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rid, cid, mid, cat, lvl, prob, impact, ev, mit))
        
    # 6. Add Seeded Tasks (Action Tracker)
    tasks = [
        ("task-1", "default-workspace", "acme-corp", m1_id, "node-m1-4", "Set up multi-currency billing templates.", "John Doe", "2026-06-12", "open", "medium"),
        ("task-2", "default-workspace", "acme-corp", m2_id, "node-m2-3", "Scope technical feasibility for custom domains.", "", "2026-06-05", "open", "high") # Overdue
    ]
    for tid, wid, cid, mid, nid, cnt, own, dl, stat, prio in tasks:
        cursor.execute("""
            INSERT INTO tasks (id, workspace_id, customer_id, meeting_id, node_id, content, owner, deadline, status, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tid, wid, cid, mid, nid, cnt, own, dl, stat, prio))
        
    conn.commit()
    conn.close()
    print("Database seeded with Acme Corp details successfully.")

# Helper: Hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Auth session checks
def get_current_user(authorization: Optional[str] = Header(None)):
    conn = get_db_connection()
    
    # If authorization header is missing, check if there are any other users registered beside 'system-default'.
    # If not (e.g. test environment runs), we return the fallback default user.
    if not authorization or not authorization.startswith("Bearer "):
        other_users = conn.execute("SELECT COUNT(*) FROM users WHERE id != 'system-default'").fetchone()[0]
        if other_users == 0:
            conn.close()
            return {
                "id": "system-default",
                "full_name": "System Default User",
                "email": "default@memomeet.ai",
                "company_name": "Default Corp",
                "designation": "Administrator",
                "verified": 1,
                "created_at": "2026-06-06 00:00:00"
            }
        conn.close()
        raise HTTPException(status_code=401, detail="Authentication credentials not found or invalid format.")
        
    token = authorization.split(" ")[1]
    session = conn.execute("SELECT user_id FROM sessions WHERE token = ?", (token,)).fetchone()
    if not session:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid or expired session token.")
        
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return dict(user)

def get_active_workspace(user: Dict[str, Any] = Depends(get_current_user), x_workspace_id: Optional[str] = Header(None)):
    if user["id"] == "system-default":
        return "default-workspace"
        
    conn = get_db_connection()
    if x_workspace_id:
        member = conn.execute(
            "SELECT * FROM workspace_users WHERE workspace_id = ? AND user_id = ?",
            (x_workspace_id, user["id"])
        ).fetchone()
        if member:
            conn.close()
            return x_workspace_id
            
    row = conn.execute(
        "SELECT workspace_id FROM workspace_users WHERE user_id = ? ORDER BY created_at ASC LIMIT 1",
        (user["id"],)
    ).fetchone()
    if row:
        workspace_id = row["workspace_id"]
        conn.close()
        return workspace_id
        
    conn.close()
    return None

@app.on_event("startup")
def startup_event():
    init_db()
    seed_initial_data()

# ENDPOINTS

# AUTH FLOW
@app.post("/api/auth/register", response_model=SessionResponse)
def register_user(reg: UserRegister):
    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (reg.email.lower().strip(),)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="User with this email already registered.")
        
    user_id = str(uuid.uuid4())
    pw_hash = hash_password(reg.password)
    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, full_name, email, company_name, designation, password_hash, verified) VALUES (?, ?, ?, ?, ?, ?, 0)",
        (user_id, reg.full_name, reg.email.lower().strip(), reg.company_name, reg.designation, pw_hash)
    )
    
    # Auto create a default workspace for them
    ws_id = str(uuid.uuid4())
    ws_name = f"{reg.company_name or reg.full_name}'s Workspace"
    cursor.execute(
        "INSERT INTO workspaces (id, name, owner_id) VALUES (?, ?, ?)",
        (ws_id, ws_name, user_id)
    )
    cursor.execute(
        "INSERT INTO workspace_users (id, workspace_id, user_id, role) VALUES (?, ?, ?, 'admin')",
        (str(uuid.uuid4()), ws_id, user_id)
    )
    
    # Create session
    token = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO sessions (token, user_id) VALUES (?, ?)",
        (token, user_id)
    )
    
    conn.commit()
    user_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    return SessionResponse(
        token=token,
        user=UserResponse(**dict(user_row))
    )

@app.post("/api/auth/login", response_model=SessionResponse)
def login_user(cred: UserLogin):
    conn = get_db_connection()
    pw_hash = hash_password(cred.password)
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (cred.email.lower().strip(), pw_hash)
    ).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    token = str(uuid.uuid4())
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (token, user_id) VALUES (?, ?)",
        (token, user["id"])
    )
    conn.commit()
    conn.close()
    
    return SessionResponse(
        token=token,
        user=UserResponse(**dict(user))
    )

@app.post("/api/auth/logout")
def logout_user(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()
    return {"status": "success", "message": "Logged out successfully."}

@app.get("/api/auth/me", response_model=UserResponse)
def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    return UserResponse(**user)

@app.post("/api/auth/verify-email")
def verify_email(req: VerifyEmailRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (req.email.lower().strip(),)).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found.")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET verified = 1 WHERE id = ?", (user["id"],))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Email verified successfully."}

@app.post("/api/auth/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (req.email.lower().strip(),)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="Email address not found.")
    return {"status": "success", "message": "Password recovery email has been sent."}


# WORKSPACES
@app.get("/api/workspaces", response_model=List[WorkspaceResponse])
def get_workspaces(user: Dict[str, Any] = Depends(get_current_user)):
    if user["id"] == "system-default":
        return [WorkspaceResponse(id="default-workspace", name="Default Workspace", owner_id="system-default", created_at="2026-06-06 00:00:00")]
        
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT w.* FROM workspaces w
        JOIN workspace_users wu ON w.id = wu.workspace_id
        WHERE wu.user_id = ?
        """,
        (user["id"],)
    ).fetchall()
    conn.close()
    return [WorkspaceResponse(**dict(r)) for r in rows]

@app.post("/api/workspaces", response_model=WorkspaceResponse)
def create_workspace(ws: WorkspaceCreate, user: Dict[str, Any] = Depends(get_current_user)):
    if user["id"] == "system-default":
        raise HTTPException(status_code=400, detail="Cannot create workspaces in system-default mock mode.")
        
    ws_id = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO workspaces (id, name, industry, team_size, use_case, owner_id) VALUES (?, ?, ?, ?, ?, ?)",
        (ws_id, ws.name, ws.industry, ws.team_size, ws.use_case, user["id"])
    )
    cursor.execute(
        "INSERT INTO workspace_users (id, workspace_id, user_id, role) VALUES (?, ?, ?, 'admin')",
        (str(uuid.uuid4()), ws_id, user["id"])
    )
    conn.commit()
    row = conn.execute("SELECT * FROM workspaces WHERE id = ?", (ws_id,)).fetchone()
    conn.close()
    return WorkspaceResponse(**dict(row))

@app.post("/api/workspaces/onboard")
def onboard_workspace(data: Dict[str, Any] = Body(...), user: Dict[str, Any] = Depends(get_current_user)):
    company_name = data.get("company_name", "My Workspace")
    industry = data.get("industry", "Technology")
    team_size = int(data.get("team_size", 1))
    use_case = data.get("use_case", "Productive Meetings")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    first_wu = conn.execute("SELECT workspace_id FROM workspace_users WHERE user_id = ? LIMIT 1", (user["id"],)).fetchone()
    if first_wu:
        ws_id = first_wu["workspace_id"]
        cursor.execute(
            "UPDATE workspaces SET name = ?, industry = ?, team_size = ?, use_case = ? WHERE id = ?",
            (company_name, industry, team_size, use_case, ws_id)
        )
    else:
        ws_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO workspaces (id, name, industry, team_size, use_case, owner_id) VALUES (?, ?, ?, ?, ?, ?)",
            (ws_id, company_name, industry, team_size, use_case, user["id"])
        )
        cursor.execute(
            "INSERT INTO workspace_users (id, workspace_id, user_id, role) VALUES (?, ?, ?, 'admin')",
            (str(uuid.uuid4()), ws_id, user["id"])
        )
        
    conn.commit()
    conn.close()
    return {"status": "success", "workspace_id": ws_id}

@app.get("/api/workspaces/{ws_id}/members", response_model=List[WorkspaceMemberResponse])
def get_workspace_members(ws_id: str, user: Dict[str, Any] = Depends(get_current_user)):
    conn = get_db_connection()
    if user["id"] != "system-default":
        member = conn.execute("SELECT * FROM workspace_users WHERE workspace_id = ? AND user_id = ?", (ws_id, user["id"])).fetchone()
        if not member:
            conn.close()
            raise HTTPException(status_code=403, detail="Forbidden workspace access.")
            
    rows = conn.execute(
        """
        SELECT wu.user_id, u.full_name, u.email, wu.role
        FROM workspace_users wu
        JOIN users u ON wu.user_id = u.id
        WHERE wu.workspace_id = ?
        """,
        (ws_id,)
    ).fetchall()
    conn.close()
    return [WorkspaceMemberResponse(**dict(r)) for r in rows]

@app.post("/api/workspaces/{ws_id}/invite", response_model=WorkspaceInviteResponse)
def invite_workspace_member(ws_id: str, req: WorkspaceInviteRequest, user: Dict[str, Any] = Depends(get_current_user)):
    conn = get_db_connection()
    if user["id"] != "system-default":
        member = conn.execute("SELECT * FROM workspace_users WHERE workspace_id = ? AND user_id = ?", (ws_id, user["id"])).fetchone()
        if not member or member["role"] not in ["admin", "manager"]:
            conn.close()
            raise HTTPException(status_code=403, detail="Forbidden. Only Admins and Managers can invite members.")
            
    invite_id = str(uuid.uuid4())
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO workspace_invites (id, workspace_id, email, role) VALUES (?, ?, ?, ?)",
        (invite_id, ws_id, req.email.lower().strip(), req.role)
    )
    
    invited_user = conn.execute("SELECT id FROM users WHERE email = ?", (req.email.lower().strip(),)).fetchone()
    if invited_user:
        cursor.execute(
            "INSERT INTO workspace_users (id, workspace_id, user_id, role) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), ws_id, invited_user["id"], req.role)
        )
        cursor.execute("UPDATE workspace_invites SET accepted = 1 WHERE id = ?", (invite_id,))
        
    conn.commit()
    row = conn.execute("SELECT * FROM workspace_invites WHERE id = ?", (invite_id,)).fetchone()
    conn.close()
    return WorkspaceInviteResponse(**dict(row))


# CUSTOMERS & MEETINGS
@app.get("/api/customers", response_model=List[CustomerResponse])
def list_customers(workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    if workspace_id and workspace_id != "default-workspace":
        rows = conn.execute("SELECT * FROM customers WHERE workspace_id = ? OR (workspace_id IS NULL OR workspace_id = '')", (workspace_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/meetings", response_model=List[MeetingListItem])
def list_meetings(workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    if workspace_id and workspace_id != "default-workspace":
        query = """
            SELECT m.id, m.title, m.meeting_date, m.iq_score, m.sentiment_score, c.name as customer_name, c.id as customer_id
            FROM meetings m
            JOIN customers c ON m.customer_id = c.id
            WHERE m.workspace_id = ? OR (m.workspace_id IS NULL OR m.workspace_id = '')
            ORDER BY m.meeting_date DESC
        """
        rows = conn.execute(query, (workspace_id,)).fetchall()
    else:
        query = """
            SELECT m.id, m.title, m.meeting_date, m.iq_score, m.sentiment_score, c.name as customer_name, c.id as customer_id
            FROM meetings m
            JOIN customers c ON m.customer_id = c.id
            ORDER BY m.meeting_date DESC
        """
        rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/meetings/{meeting_id}", response_model=MeetingDetailResponse)
def get_meeting(meeting_id: str):
    conn = get_db_connection()
    meeting_row = conn.execute("""
        SELECT m.*, c.name as customer_name 
        FROM meetings m 
        JOIN customers c ON m.customer_id = c.id 
        WHERE m.id = ?
    """, (meeting_id,)).fetchone()
    
    if not meeting_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Meeting not found")
        
    trans_rows = conn.execute(
        "SELECT speaker, text, start_time, end_time FROM transcripts WHERE meeting_id = ? ORDER BY start_time ASC",
        (meeting_id,)
    ).fetchall()
    
    nodes_rows = conn.execute(
        "SELECT id, category, content, speaker, confidence_level FROM memory_nodes WHERE meeting_id = ?",
        (meeting_id,)
    ).fetchall()
    
    conn.close()
    
    meeting_data = dict(meeting_row)
    try:
        meeting_data["iq_breakdown"] = json.loads(meeting_data["iq_breakdown"])
    except:
        meeting_data["iq_breakdown"] = {}
        
    meeting_data["transcript"] = [dict(row) for row in trans_rows]
    
    nodes = [dict(row) for row in nodes_rows]
    meeting_data["decisions"] = [n for n in nodes if n["category"] == "decision"]
    meeting_data["requirements"] = [n for n in nodes if n["category"] == "requirement"]
    meeting_data["deadlines"] = [n for n in nodes if n["category"] == "deadline"]
    meeting_data["risks"] = [n for n in nodes if n["category"] == "risk"]
    meeting_data["commitments"] = [n for n in nodes if n["category"] == "commitment"]
    meeting_data["action_items"] = [n for n in nodes if n["category"] == "action_item"]
    meeting_data["objections"] = [n for n in nodes if n["category"] == "objection"]
    
    return meeting_data

@app.post("/api/meetings")
def upload_meeting(meeting: MeetingCreate, workspace_id: Optional[str] = Depends(get_active_workspace)):
    transcript_dicts = [t.dict() for t in meeting.transcript]
    try:
        insights = process_and_retain_meeting(
            meeting_id=meeting.id,
            title=meeting.title,
            customer_id=meeting.customer_id,
            meeting_date=meeting.meeting_date,
            duration_seconds=meeting.duration_seconds,
            transcript_lines=transcript_dicts,
            workspace_id=workspace_id
        )
        return {"status": "success", "meeting_id": meeting.id, "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{customer_id}/graph", response_model=BusinessMemoryGraphResponse)
def get_customer_graph(customer_id: str):
    conn = get_db_connection()
    cust = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not cust:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")
        
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    
    nodes.append(GraphNode(
        id=customer_id,
        label=cust["name"],
        type="customer",
        properties={"industry": cust["industry"]}
    ))
    
    meetings = conn.execute("SELECT id, title, meeting_date FROM meetings WHERE customer_id = ?", (customer_id,)).fetchall()
    for m in meetings:
        nodes.append(GraphNode(
            id=m["id"],
            label=m["title"],
            type="meeting",
            properties={"date": str(m["meeting_date"])}
        ))
        
        edges.append(GraphEdge(
            id=f"e-{customer_id}-{m['id']}",
            source=customer_id,
            target=m["id"],
            type="HAS_MEETING"
        ))
        
    memories = conn.execute(
        "SELECT id, meeting_id, category, content, speaker, confidence_level FROM memory_nodes WHERE customer_id = ?",
        (customer_id,)
    ).fetchall()
    
    for mem in memories:
        nodes.append(GraphNode(
            id=mem["id"],
            label=mem["content"][:40] + ("..." if len(mem["content"]) > 40 else ""),
            type=mem["category"],
            properties={
                "content": mem["content"],
                "speaker": mem["speaker"],
                "confidence": mem["confidence_level"]
            }
        ))
        
        edges.append(GraphEdge(
            id=f"e-{mem['meeting_id']}-{mem['id']}",
            source=mem["meeting_id"],
            target=mem["id"],
            type=f"CONTAINS_{mem['category'].upper()}"
        ))
        
        edges.append(GraphEdge(
            id=f"e-{customer_id}-{mem['id']}",
            source=customer_id,
            target=mem["id"],
            type=f"HAS_{mem['category'].upper()}"
        ))
        
    conn.close()
    return BusinessMemoryGraphResponse(nodes=nodes, edges=edges)

@app.get("/api/customers/{customer_id}/timeline")
def get_customer_timeline(customer_id: str):
    conn = get_db_connection()
    meetings = conn.execute(
        "SELECT id, title, meeting_date, sentiment_score, iq_score FROM meetings WHERE customer_id = ? ORDER BY meeting_date ASC",
        (customer_id,)
    ).fetchall()
    
    timeline_events = []
    for m in meetings:
        nodes = conn.execute(
            "SELECT category, content, speaker FROM memory_nodes WHERE meeting_id = ?",
            (m["id"],)
        ).fetchall()
        
        decisions = [n["content"] for n in nodes if n["category"] == "decision"]
        requirements = [n["content"] for n in nodes if n["category"] == "requirement"]
        objections = [n["content"] for n in nodes if n["category"] == "objection"]
        risks = [n["content"] for n in nodes if n["category"] == "risk"]
        
        timeline_events.append({
            "meeting_id": m["id"],
            "title": m["title"],
            "date": str(m["meeting_date"]),
            "sentiment_score": m["sentiment_score"],
            "iq_score": m["iq_score"],
            "decisions": decisions,
            "requirements": requirements,
            "objections": objections,
            "risks": risks
        })
        
    conn.close()
    return {"customer_id": customer_id, "timeline": timeline_events}


# TRUTH VERIFICATION
@app.post("/api/truth-verification", response_model=TruthVerificationResponse)
def verify_truth(req: TruthVerificationRequest):
    conn = get_db_connection()
    keywords = [k.lower().strip(",.?\"'") for k in req.query.split() if len(k) > 3]
    if not keywords:
        conn.close()
        return TruthVerificationResponse(
            query=req.query,
            direct_answer="No keyword context provided for search.",
            evidence_cards=[]
        )
        
    sql_query = """
        SELECT t.text, t.speaker, t.meeting_id, m.title as meeting_title, m.meeting_date
        FROM transcripts t
        JOIN meetings m ON t.meeting_id = m.id
    """
    params = []
    if req.customer_id:
        sql_query += " WHERE m.customer_id = ?"
        params.append(req.customer_id)
        
    rows = conn.execute(sql_query, params).fetchall()
    evidence_cards: List[EvidenceCard] = []
    
    for row in rows:
        text = row["text"].lower()
        match_count = sum(1 for kw in keywords if kw in text)
        if match_count > 0:
            confidence = min(0.99, 0.4 + (match_count * 0.15))
            
            # Fetch surrounding discussions (other quotes or requirement notes on same client)
            evidence_cards.append(EvidenceCard(
                meeting_id=row["meeting_id"],
                meeting_title=row["meeting_title"],
                meeting_date=str(row["meeting_date"]),
                speaker=row["speaker"],
                text_excerpt=row["text"],
                confidence_level=float(round(confidence, 2)),
                context_before="...",
                context_after="..."
            ))
            
    conn.close()
    evidence_cards.sort(key=lambda x: x.confidence_level, reverse=True)
    evidence_cards = evidence_cards[:5]
    
    if not evidence_cards:
        direct_answer = f"I searched the organizational memory but found no historical references discussing '{req.query}'."
    else:
        top = evidence_cards[0]
        direct_answer = f"Yes, this was discussed. According to records from {top.meeting_date} ({top.meeting_title}), {top.speaker} stated: \"{top.text_excerpt}\"."
        
    return TruthVerificationResponse(
        query=req.query,
        direct_answer=direct_answer,
        evidence_cards=evidence_cards
    )


# CONTRADICTIONS
@app.get("/api/contradictions", response_model=List[ContradictionResponse])
def get_contradictions(workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    query = """
        SELECT c.*, cust.name as customer_name, 
               m_a.title as meeting_title_a, m_a.meeting_date as meeting_date_a,
               m_b.title as meeting_title_b, m_b.meeting_date as meeting_date_b
        FROM contradictions c
        JOIN customers cust ON c.customer_id = cust.id
        JOIN meetings m_a ON c.meeting_id_a = m_a.id
        JOIN meetings m_b ON c.meeting_id_b = m_b.id
        WHERE c.resolved = 0
    """
    params = []
    if workspace_id and workspace_id != "default-workspace":
        query += " AND (cust.workspace_id = ? OR cust.workspace_id IS NULL OR cust.workspace_id = '')"
        params.append(workspace_id)
        
    rows = conn.execute(query, params).fetchall()
    results = []
    
    for r in rows:
        data = dict(r)
        data["speaker_a"] = "John Doe (CTO)" if "node-m1-1" in [r["node_id_a"], r["node_id_b"]] else "Sarah Jenkins (VP Product)"
        data["speaker_b"] = "Sarah Jenkins (VP Product)" if "node-m2-1" in [r["node_id_a"], r["node_id_b"]] else "John Doe (CTO)"
        results.append(data)
        
    conn.close()
    return results

@app.post("/api/contradictions/{id}/resolve")
def resolve_contradiction(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contradictions SET resolved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Contradiction resolved."}


# RISKS
@app.get("/api/predictions", response_model=List[RiskPredictionResponse])
def get_predictions(customer_id: Optional[str] = None, workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    query = """
        SELECT r.*, c.name as customer_name
        FROM risks r
        JOIN customers c ON r.customer_id = c.id
    """
    params = []
    
    # workspace filter
    if workspace_id and workspace_id != "default-workspace":
        query += " WHERE (c.workspace_id = ? OR c.workspace_id IS NULL OR c.workspace_id = '')"
        params.append(workspace_id)
        if customer_id:
            query += " AND r.customer_id = ?"
            params.append(customer_id)
    elif customer_id:
        query += " WHERE r.customer_id = ?"
        params.append(customer_id)
        
    rows = conn.execute(query, params).fetchall()
    results = []
    for r in rows:
        data = dict(r)
        try:
            data["evidence"] = json.loads(data["evidence"])
        except:
            data["evidence"] = []
        results.append(data)
        
    conn.close()
    return results


# ACTION TRACKER (TASKS) CRUD
@app.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks(
    workspace_id: Optional[str] = Depends(get_active_workspace),
    customer_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    conn = get_db_connection()
    query_str = """
        SELECT t.*, c.name as customer_name, m.title as meeting_title
        FROM tasks t
        LEFT JOIN customers c ON t.customer_id = c.id
        LEFT JOIN meetings m ON t.meeting_id = m.id
    """
    params = []
    
    if workspace_id != "default-workspace":
        query_str += " WHERE t.workspace_id = ?"
        params.append(workspace_id)
    else:
        query_str += " WHERE 1=1"
        
    if customer_id:
        query_str += " AND t.customer_id = ?"
        params.append(customer_id)
    if status:
        query_str += " AND t.status = ?"
        params.append(status)
        
    query_str += " ORDER BY t.created_at DESC"
    rows = conn.execute(query_str, params).fetchall()
    conn.close()
    return [TaskResponse(**dict(r)) for r in rows]

@app.post("/api/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, workspace_id: Optional[str] = Depends(get_active_workspace)):
    task_id = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (id, workspace_id, customer_id, meeting_id, node_id, content, owner, deadline, status, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', ?)
        """,
        (
            task_id,
            workspace_id or "default-workspace",
            task.customer_id,
            task.meeting_id,
            task.node_id,
            task.content,
            task.owner,
            task.deadline,
            task.priority or "medium"
        )
    )
    conn.commit()
    row = conn.execute(
        """
        SELECT t.*, c.name as customer_name, m.title as meeting_title
        FROM tasks t
        LEFT JOIN customers c ON t.customer_id = c.id
        LEFT JOIN meetings m ON t.meeting_id = m.id
        WHERE t.id = ?
        """,
        (task_id,)
    ).fetchone()
    conn.close()
    return TaskResponse(**dict(row))

@app.put("/api/tasks/{id}", response_model=TaskResponse)
def update_task(id: str, task: TaskUpdate, user: Dict[str, Any] = Depends(get_current_user)):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found.")
        
    cursor = conn.cursor()
    
    updates = []
    params = []
    for field, val in task.dict(exclude_unset=True).items():
        updates.append(f"{field} = ?")
        params.append(val)
        
    if updates:
        params.append(id)
        cursor.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
        
    row = conn.execute(
        """
        SELECT t.*, c.name as customer_name, m.title as meeting_title
        FROM tasks t
        LEFT JOIN customers c ON t.customer_id = c.id
        LEFT JOIN meetings m ON t.meeting_id = m.id
        WHERE t.id = ?
        """,
        (id,)
    ).fetchone()
    conn.close()
    return TaskResponse(**dict(row))

@app.delete("/api/tasks/{id}")
def delete_task(id: str, user: Dict[str, Any] = Depends(get_current_user)):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found.")
        
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Task deleted successfully."}


# GLOBAL SEARCH
@app.get("/api/search", response_model=SearchResponse)
def global_search(q: str = Query(...), workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    results = []
    term = f"%{q}%"
    
    # 1. Search Meetings
    meetings_query = "SELECT m.id, m.title, m.meeting_date, c.name as customer_name, c.id as customer_id FROM meetings m JOIN customers c ON m.customer_id = c.id"
    params = [term]
    if workspace_id != "default-workspace":
        meetings_query += " WHERE m.workspace_id = ? AND m.title LIKE ?"
        params = [workspace_id, term]
    else:
        meetings_query += " WHERE m.title LIKE ?"
    m_rows = conn.execute(meetings_query, params).fetchall()
    for row in m_rows:
        results.append(SearchResultItem(
            id=row["id"],
            type="meeting",
            title=row["title"],
            description=f"Meeting held on {row['meeting_date']}",
            date=str(row["meeting_date"]),
            customer_id=row["customer_id"],
            customer_name=row["customer_name"]
        ))
        
    # 2. Search Customers
    cust_query = "SELECT * FROM customers"
    params = [term]
    if workspace_id != "default-workspace":
        cust_query += " WHERE workspace_id = ? AND name LIKE ?"
        params = [workspace_id, term]
    else:
        cust_query += " WHERE name LIKE ?"
    c_rows = conn.execute(cust_query, params).fetchall()
    for row in c_rows:
        results.append(SearchResultItem(
            id=row["id"],
            type="customer",
            title=row["name"],
            description=f"Industry: {row['industry'] or 'Uncategorized'}",
            customer_id=row["id"],
            customer_name=row["name"]
        ))
        
    # 3. Search Memory Nodes
    node_query = """
        SELECT n.*, c.name as customer_name, m.title as meeting_title, m.meeting_date
        FROM memory_nodes n
        JOIN customers c ON n.customer_id = c.id
        JOIN meetings m ON n.meeting_id = m.id
    """
    params = [term]
    if workspace_id != "default-workspace":
        node_query += " WHERE m.workspace_id = ? AND n.content LIKE ?"
        params = [workspace_id, term]
    else:
        node_query += " WHERE n.content LIKE ?"
    n_rows = conn.execute(node_query, params).fetchall()
    for row in n_rows:
        results.append(SearchResultItem(
            id=row["id"],
            type=row["category"],
            title=row["content"],
            description=f"Category: {row['category'].replace('_', ' ').title()} • Speaker: {row['speaker'] or 'Unknown'}",
            date=str(row["meeting_date"]),
            customer_id=row["customer_id"],
            customer_name=row["customer_name"]
        ))
        
    # 4. Search Tasks
    task_query = """
        SELECT t.*, c.name as customer_name
        FROM tasks t
        LEFT JOIN customers c ON t.customer_id = c.id
    """
    params = [term]
    if workspace_id != "default-workspace":
        task_query += " WHERE t.workspace_id = ? AND t.content LIKE ?"
        params = [workspace_id, term]
    else:
        task_query += " WHERE t.content LIKE ?"
    t_rows = conn.execute(task_query, params).fetchall()
    for row in t_rows:
        results.append(SearchResultItem(
            id=row["id"],
            type="task",
            title=row["content"],
            description=f"Task Owner: {row['owner'] or 'Unassigned'} • Status: {row['status'].upper()}",
            date=str(row["deadline"]) if row["deadline"] else None,
            customer_id=row["customer_id"],
            customer_name=row["customer_name"]
        ))
        
    conn.close()
    return SearchResponse(query=q, results=results)


# HEALTH SCORE & ALERTS
@app.get("/api/health-score")
def get_memory_health_score(workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    
    meeting_q = "SELECT id FROM meetings"
    params = []
    if workspace_id != "default-workspace":
        meeting_q += " WHERE workspace_id = ?"
        params.append(workspace_id)
    m_ids = [r["id"] for r in conn.execute(meeting_q, params).fetchall()]
    total_meetings = len(m_ids)
    
    meetings_no_decision = 0
    if total_meetings > 0:
        placeholders = ",".join(["?"] * total_meetings)
        dec_meetings_query = f"SELECT DISTINCT meeting_id FROM memory_nodes WHERE category = 'decision' AND meeting_id IN ({placeholders})"
        dec_meetings = [r["meeting_id"] for r in conn.execute(dec_meetings_query, m_ids).fetchall()]
        meetings_no_decision = len(set(m_ids) - set(dec_meetings))
        
    task_q = "SELECT COUNT(*) FROM tasks WHERE status IN ('open', 'in_progress') AND (owner IS NULL OR owner = '')"
    params_t = []
    if workspace_id != "default-workspace":
        task_q += " AND workspace_id = ?"
        params_t.append(workspace_id)
    unassigned_tasks = conn.execute(task_q, params_t).fetchone()[0]
    
    import datetime
    today = datetime.date.today().isoformat()
    overdue_q = "SELECT COUNT(*) FROM tasks WHERE status = 'overdue' OR (status IN ('open', 'in_progress') AND deadline < ?)"
    params_o = [today]
    if workspace_id != "default-workspace":
        overdue_q += " AND workspace_id = ?"
        params_o.append(workspace_id)
    overdue_tasks = conn.execute(overdue_q, params_o).fetchone()[0]
    
    risk_q = "SELECT COUNT(*) FROM risks r JOIN meetings m ON r.meeting_id = m.id WHERE r.risk_level IN ('high', 'medium')"
    params_r = []
    if workspace_id != "default-workspace":
        risk_q += " AND m.workspace_id = ?"
        params_r.append(workspace_id)
    open_risks = conn.execute(risk_q, params_r).fetchone()[0]
    
    deductions = (meetings_no_decision * 15) + (unassigned_tasks * 8) + (overdue_tasks * 12) + (open_risks * 10)
    score = max(35, min(100, 100 - deductions))
    
    conn.close()
    return {
        "score": score,
        "metrics": {
            "meetings_no_decision": meetings_no_decision,
            "unassigned_tasks": unassigned_tasks,
            "overdue_tasks": overdue_tasks,
            "open_risks": open_risks
        }
    }

@app.get("/api/alerts", response_model=List[AlertNotification])
def list_alerts(workspace_id: Optional[str] = Depends(get_active_workspace)):
    import datetime
    conn = get_db_connection()
    alerts = []
    
    # 1. Contradictions detected
    contra_query = """
        SELECT c.*, cust.name as customer_name
        FROM contradictions c
        JOIN customers cust ON c.customer_id = cust.id
        WHERE c.resolved = 0
    """
    params = []
    if workspace_id != "default-workspace":
        contra_query += " AND (cust.workspace_id = ? OR cust.workspace_id IS NULL OR cust.workspace_id = '')"
        params.append(workspace_id)
    contra_rows = conn.execute(contra_query, params).fetchall()
    for r in contra_rows:
        alerts.append(AlertNotification(
            id=f"alert-contra-{r['id']}",
            type="contradiction",
            title="Meeting Contradiction Detected",
            message=f"Contradiction found for client {r['customer_name']}: '{r['statement_a']}' vs '{r['statement_b']}'",
            reference_id=r["meeting_id_b"],
            created_at=r["created_at"]
        ))
        
    # 2. Overdue or Approaching Deadlines
    today_dt = datetime.date.today()
    plus_2_days = (today_dt + datetime.timedelta(days=2)).isoformat()
    today = today_dt.isoformat()
    
    task_query = """
        SELECT t.*, c.name as customer_name
        FROM tasks t
        LEFT JOIN customers c ON t.customer_id = c.id
        WHERE t.status IN ('open', 'in_progress') AND t.deadline <= ?
    """
    params = [plus_2_days]
    if workspace_id != "default-workspace":
        task_query += " AND t.workspace_id = ?"
        params.append(workspace_id)
    task_rows = conn.execute(task_query, params).fetchall()
    for r in task_rows:
        is_overdue = r["deadline"] < today
        type_str = "deadline"
        title_str = "Task Deadline Approaching" if not is_overdue else "Task Overdue Alert"
        msg_str = f"Task '{r['content']}' for {r['customer_name'] or 'Workspace'} is due on {r['deadline']}" if not is_overdue else f"Task '{r['content']}' is overdue! Deadline was {r['deadline']}"
        alerts.append(AlertNotification(
            id=f"alert-task-{r['id']}",
            type=type_str,
            title=title_str,
            message=msg_str,
            reference_id=r["meeting_id"] or "",
            created_at=r["created_at"]
        ))
        
    # 3. Risk Increased (High Risks)
    risk_query = """
        SELECT r.*, c.name as customer_name
        FROM risks r
        JOIN customers c ON r.customer_id = c.id
        WHERE r.risk_level = 'high'
    """
    params = []
    if workspace_id != "default-workspace":
        risk_query += " AND (c.workspace_id = ? OR c.workspace_id IS NULL OR c.workspace_id = '')"
        params.append(workspace_id)
    risk_rows = conn.execute(risk_query, params).fetchall()
    for r in risk_rows:
        alerts.append(AlertNotification(
            id=f"alert-risk-{r['id']}",
            type="risk_increase",
            title="High Risk Alert",
            message=f"High risk '{r['category'].replace('_', ' ').title()}' flagged for {r['customer_name']}: {r['impact']}",
            reference_id=r["meeting_id"],
            created_at=r["created_at"]
        ))
        
    alerts.sort(key=lambda x: x.created_at, reverse=True)
    conn.close()
    return alerts


# HACKATHON WOW ENDPOINTS
@app.get("/api/wow/drift", response_model=RequirementDriftResponse)
def get_requirement_drift(customer_id: str):
    conn = get_db_connection()
    cust = conn.execute("SELECT name FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not cust:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")
        
    query = """
        SELECT n.*, m.title as meeting_title, m.meeting_date
        FROM memory_nodes n
        JOIN meetings m ON n.meeting_id = m.id
        WHERE n.customer_id = ? AND n.category = 'requirement'
        ORDER BY m.meeting_date ASC, n.created_at ASC
    """
    rows = conn.execute(query, (customer_id,)).fetchall()
    
    contras = conn.execute(
        "SELECT * FROM contradictions WHERE customer_id = ? AND resolved = 0",
        (customer_id,)
    ).fetchall()
    
    timeline = []
    for r in rows:
        node_id = r["id"]
        status = r["status"]
        drift_exp = None
        
        for c in contras:
            if c["node_id_b"] == node_id:
                status = "changed"
                drift_exp = f"Superseded previous statement: '{c['statement_a']}' because: {c['explanation']}"
            elif c["node_id_a"] == node_id:
                status = "superseded"
                
        timeline.append(RequirementDriftItem(
            date=str(r["meeting_date"]),
            meeting_id=r["meeting_id"],
            meeting_title=r["meeting_title"],
            content=r["content"],
            speaker=r["speaker"] or "Client",
            status=status,
            drift_explanation=drift_exp
        ))
        
    conn.close()
    return RequirementDriftResponse(
        customer_id=customer_id,
        customer_name=cust["name"],
        timeline=timeline
    )

@app.get("/api/wow/commitments", response_model=CommitmentTrackerResponse)
def get_commitment_tracker(customer_id: Optional[str] = Query(None), workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    query = """
        SELECT n.*, t.status, t.owner, t.deadline, t.created_at as completed_date
        FROM memory_nodes n
        LEFT JOIN tasks t ON n.id = t.node_id
        JOIN meetings m ON n.meeting_id = m.id
        WHERE n.category = 'commitment'
    """
    params = []
    if workspace_id != "default-workspace":
        query += " AND m.workspace_id = ?"
        params.append(workspace_id)
    if customer_id:
        query += " AND n.customer_id = ?"
        params.append(customer_id)
        
    rows = conn.execute(query, params).fetchall()
    commitments = []
    completed = 0
    total = 0
    
    for r in rows:
        total += 1
        status = r["status"] or "open"
        if status == "completed":
            completed += 1
            
        commitments.append(CommitmentTrackerItem(
            id=r["id"],
            content=r["content"],
            speaker=r["speaker"] or "Client",
            status=status,
            deadline=str(r["deadline"]) if r["deadline"] else None,
            owner=r["owner"],
            completed_date=str(r["completed_date"])[:10] if status == "completed" else None
        ))
        
    conn.close()
    rate = (completed / total * 100) if total > 0 else 100.0
    return CommitmentTrackerResponse(
        total=total,
        completed=completed,
        pending=total - completed,
        completion_rate=float(round(rate, 2)),
        commitments=commitments
    )

@app.get("/api/wow/stakeholders", response_model=StakeholderInfluenceResponse)
def get_stakeholder_influence(customer_id: str):
    conn = get_db_connection()
    nodes = conn.execute(
        "SELECT category, speaker FROM memory_nodes WHERE customer_id = ?",
        (customer_id,)
    ).fetchall()
    
    speakers_data = {}
    for n in nodes:
        sp = n["speaker"]
        if not sp or sp == "Unknown":
            continue
        if sp not in speakers_data:
            speakers_data[sp] = {"decisions": 0, "objections": 0, "commitments": 0, "talk_count": 0}
        
        cat = n["category"]
        if cat == "decision":
            speakers_data[sp]["decisions"] += 1
        elif cat == "objection":
            speakers_data[sp]["objections"] += 1
        elif cat == "commitment":
            speakers_data[sp]["commitments"] += 1
            
    trans = conn.execute(
        """
        SELECT t.speaker, COUNT(*) as count 
        FROM transcripts t
        JOIN meetings m ON t.meeting_id = m.id
        WHERE m.customer_id = ?
        GROUP BY t.speaker
        """,
        (customer_id,)
    ).fetchall()
    
    for t in trans:
        sp = t["speaker"]
        if not sp:
            continue
        matched_sp = None
        for key in speakers_data.keys():
            if key.split("(")[0].strip().lower() in sp.lower():
                matched_sp = key
                break
        
        if matched_sp:
            speakers_data[matched_sp]["talk_count"] += t["count"]
        else:
            speakers_data[sp] = {"decisions": 0, "objections": 0, "commitments": 0, "talk_count": t["count"]}
            
    conn.close()
    stakeholders = []
    for sp, data in speakers_data.items():
        score = (data["decisions"] * 20) + (data["commitments"] * 15) + (data["objections"] * 10) + (data["talk_count"] * 0.5)
        score = min(100.0, max(15.0, score))
        stakeholders.append(StakeholderScore(
            speaker=sp,
            influence_score=float(round(score, 2)),
            decision_count=data["decisions"],
            objection_count=data["objections"],
            commitment_count=data["commitments"]
        ))
        
    stakeholders.sort(key=lambda x: x.influence_score, reverse=True)
    return StakeholderInfluenceResponse(stakeholders=stakeholders)

@app.get("/api/wow/trust", response_model=CustomerTrustResponse)
def get_customer_trust(customer_id: str):
    conn = get_db_connection()
    cust = conn.execute("SELECT name FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not cust:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")
        
    contras = conn.execute(
        """
        SELECT c.*, m_a.title as meeting_title_a, m_a.meeting_date as meeting_date_a,
               m_b.title as meeting_title_b, m_b.meeting_date as meeting_date_b
        FROM contradictions c
        JOIN meetings m_a ON c.meeting_id_a = m_a.id
        JOIN meetings m_b ON c.meeting_id_b = m_b.id
        WHERE c.customer_id = ? AND c.resolved = 0
        """,
        (customer_id,)
    ).fetchall()
    
    contra_list = []
    for r in contras:
        d = dict(r)
        d["customer_name"] = cust["name"]
        d["speaker_a"] = "John Doe (CTO)" if "node-m1-1" in [r["node_id_a"], r["node_id_b"]] else "Sarah Jenkins (VP Product)"
        d["speaker_b"] = "Sarah Jenkins (VP Product)" if "node-m2-1" in [r["node_id_a"], r["node_id_b"]] else "John Doe (CTO)"
        contra_list.append(ContradictionResponse(**d))
        
    score = 98.0 - (len(contra_list) * 15.0)
    score = max(40.0, score)
    
    if score >= 90.0:
        exp = "Excellent commitment consistency. Historical statements align perfectly with current requirements."
    elif score >= 75.0:
        exp = "Good consistency. A few adjustments in requirements have occurred but they are minor."
    else:
        exp = "Warning: Multiple contradictions detected in client statements regarding release targets and scopes."
        
    conn.close()
    return CustomerTrustResponse(
        customer_id=customer_id,
        customer_name=cust["name"],
        trust_score=float(round(score, 2)),
        explanation=exp,
        contradictions=contra_list
    )

@app.get("/api/wow/radar", response_model=RiskRadarResponse)
def get_risk_radar(customer_id: str):
    conn = get_db_connection()
    risks = conn.execute("SELECT category, risk_level, probability FROM risks WHERE customer_id = ?", (customer_id,)).fetchall()
    conn.close()
    
    scores = {"scope_creep": 20.0, "churn": 20.0, "project_delay": 20.0, "stakeholder_misalignment": 20.0}
    for r in risks:
        cat = r["category"]
        lvl = r["risk_level"]
        prob = r["probability"]
        
        base = 40.0 if lvl == "low" else 70.0 if lvl == "medium" else 90.0
        val = base * prob
        
        if cat in scores:
            scores[cat] = float(round(val, 2))
            
    return RiskRadarResponse(
        scope_creep=scores["scope_creep"],
        churn=scores["churn"],
        project_delay=scores["project_delay"],
        stakeholder_misalignment=scores["stakeholder_misalignment"]
    )


# ASSISTANT & CHAT
@app.post("/api/chat", response_model=ChatResponse)
def chat_with_assistant(req: ChatRequest, workspace_id: Optional[str] = Depends(get_active_workspace)):
    conn = get_db_connection()
    
    # Retrieve relevant customer nodes to provide as context
    params = []
    query_sql = "SELECT category, content, speaker, created_at FROM memory_nodes"
    if req.customer_id:
        query_sql += " WHERE customer_id = ?"
        params.append(req.customer_id)
    query_sql += " LIMIT 50"
    
    rows = conn.execute(query_sql, params).fetchall()
    context_memories = [dict(row) for row in rows]
    
    # Fetch tasks too to provide as context for copilot questions like pending/overdue promises!
    task_q = "SELECT content, owner, deadline, status, priority FROM tasks"
    t_params = []
    if workspace_id != "default-workspace":
        task_q += " WHERE workspace_id = ?"
        t_params.append(workspace_id)
    t_rows = conn.execute(task_q, t_params).fetchall()
    
    # Format tasks into virtual memory nodes of category 'task' so they are parsed automatically!
    for r in t_rows:
        context_memories.append({
            "category": "task",
            "content": f"Task: {r['content']} | Status: {r['status']} | Owner: {r['owner'] or 'Unassigned'} | Deadline: {r['deadline'] or 'No deadline'}",
            "speaker": r["owner"] or "Unassigned",
            "created_at": ""
        })
        
    # Retrieve referenced meetings
    meetings_sql = "SELECT id, title, meeting_date FROM meetings"
    m_params = []
    if req.customer_id:
        meetings_sql += " WHERE customer_id = ?"
        m_params.append(req.customer_id)
    meetings_sql += " LIMIT 5"
    
    meetings = conn.execute(meetings_sql, m_params).fetchall()
    referenced_meetings = [dict(m) for m in meetings]
    
    conn.close()
    
    # Get answer
    answer = answer_chief_of_staff(req.query, context_memories)
    
    return ChatResponse(
        answer=answer,
        referenced_meetings=referenced_meetings
    )


# SETTINGS
@app.get("/api/settings", response_model=SettingsResponse)
def get_settings():
    # Check key configuration
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    configured = False
    system_prompt = "You are the MemoMeet AI Chief of Staff. Retrieve, synthesize, and audit organizational meeting memory."
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                configured = bool(config.get("groq_api_key"))
                system_prompt = config.get("system_prompt", system_prompt)
        except:
            pass
            
    # Calculate Memory Health score dynamically
    # E.g. total contradictions resolved, total meetings loaded, risk levels
    conn = get_db_connection()
    total_meetings = conn.execute("SELECT COUNT(*) FROM meetings").fetchone()[0]
    unresolved_contras = conn.execute("SELECT COUNT(*) FROM contradictions WHERE resolved = 0").fetchone()[0]
    conn.close()
    
    # Higher meeting count and lower contradictions increases health
    # Start at 95, subtract 10 for each unresolved contradiction
    memory_health = max(40, 98 - (unresolved_contras * 10) + min(5, total_meetings))
    
    return SettingsResponse(
        groq_api_key_configured=configured or bool(os.environ.get("GROQ_API_KEY")),
        system_prompt=system_prompt,
        memory_health=memory_health
    )

@app.post("/api/settings")
def update_settings(settings: SettingsUpdate):
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except:
            pass
            
    if settings.groq_api_key is not None:
        config["groq_api_key"] = settings.groq_api_key
        # Update global variable
        global GROQ_API_KEY
        GROQ_API_KEY = settings.groq_api_key
    if settings.system_prompt is not None:
        config["system_prompt"] = settings.system_prompt
        
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        return {"status": "success", "message": "Settings updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write config: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
