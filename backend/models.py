from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    industry: Optional[str] = None

class CustomerCreate(CustomerBase):
    id: str

class CustomerResponse(CustomerBase):
    id: str
    created_at: str

# Transcript schemas
class TranscriptLine(BaseModel):
    speaker: str
    text: str
    start_time: Optional[float] = 0.0
    end_time: Optional[float] = 0.0

# Meeting schemas
class MeetingCreate(BaseModel):
    id: str
    title: str
    customer_id: str
    meeting_date: str  # YYYY-MM-DD
    duration_seconds: int
    transcript: List[TranscriptLine]

class MeetingListItem(BaseModel):
    id: str
    title: str
    customer_name: str
    customer_id: str
    meeting_date: str
    iq_score: int
    sentiment_score: float

class MeetingDetailResponse(BaseModel):
    id: str
    title: str
    customer_id: str
    customer_name: str
    meeting_date: str
    duration_seconds: int
    iq_score: int
    iq_breakdown: Dict[str, Any]
    sentiment_score: float
    transcript: List[TranscriptLine]
    decisions: List[Dict[str, Any]]
    requirements: List[Dict[str, Any]]
    deadlines: List[Dict[str, Any]]
    risks: List[Dict[str, Any]]
    commitments: List[Dict[str, Any]]
    action_items: List[Dict[str, Any]]
    objections: List[Dict[str, Any]]

# Graph schemas
class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # 'customer', 'meeting', 'decision', 'requirement', 'deadline', 'risk', 'action_item', 'objection', 'stakeholder'
    properties: Dict[str, Any]

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str  # 'HAS_REQUIREMENT', 'HAS_RISK', 'DECIDED', 'DEADLINE_OF', 'ASSIGNED_TO', 'ATTENDED'

class BusinessMemoryGraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# Truth Verification schemas
class TruthVerificationRequest(BaseModel):
    query: str
    customer_id: Optional[str] = None

class EvidenceCard(BaseModel):
    meeting_id: str
    meeting_title: str
    meeting_date: str
    speaker: str
    text_excerpt: str
    confidence_level: float
    context_before: Optional[str] = None
    context_after: Optional[str] = None

class TruthVerificationResponse(BaseModel):
    query: str
    direct_answer: str
    evidence_cards: List[EvidenceCard]

# Contradiction schemas
class ContradictionResponse(BaseModel):
    id: str
    customer_id: str
    customer_name: str
    statement_a: str
    statement_b: str
    meeting_title_a: str
    meeting_date_a: str
    meeting_title_b: str
    meeting_date_b: str
    speaker_a: str
    speaker_b: str
    explanation: str
    severity: str
    created_at: str

# Risk Prediction schemas
class RiskPredictionResponse(BaseModel):
    id: str
    customer_id: str
    customer_name: str
    category: str  # 'churn', 'project_delay', 'scope_creep', 'stakeholder_misalignment'
    risk_level: str  # 'high', 'medium', 'low'
    probability: float
    impact: str
    evidence: List[str]
    mitigation: str
    created_at: str

# Assistant/Chat schemas
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    query: str
    customer_id: Optional[str] = None
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    answer: str
    referenced_meetings: List[Dict[str, Any]]

# Settings schemas
class SettingsResponse(BaseModel):
    groq_api_key_configured: bool
    system_prompt: str
    memory_health: int

class SettingsUpdate(BaseModel):
    groq_api_key: Optional[str] = None
    system_prompt: Optional[str] = None

# Auth schemas
class UserRegister(BaseModel):
    full_name: str
    email: str
    company_name: Optional[str] = None
    designation: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    company_name: Optional[str] = None
    designation: Optional[str] = None
    verified: int
    created_at: str

class ForgotPasswordRequest(BaseModel):
    email: str

class VerifyEmailRequest(BaseModel):
    email: str
    code: str

class SessionResponse(BaseModel):
    token: str
    user: UserResponse

# Workspace schemas
class WorkspaceCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    team_size: Optional[int] = None
    use_case: Optional[str] = None

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    industry: Optional[str] = None
    team_size: Optional[int] = None
    use_case: Optional[str] = None
    owner_id: str
    created_at: str

class WorkspaceInviteRequest(BaseModel):
    email: str
    role: str # 'admin', 'manager', 'viewer'

class WorkspaceInviteResponse(BaseModel):
    id: str
    workspace_id: str
    email: str
    role: str
    accepted: int
    created_at: str

class WorkspaceMemberResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    role: str

# Task schemas
class TaskCreate(BaseModel):
    content: str
    owner: Optional[str] = None
    deadline: Optional[str] = None # YYYY-MM-DD
    priority: Optional[str] = "medium" # 'low', 'medium', 'high'
    customer_id: Optional[str] = None
    meeting_id: Optional[str] = None
    node_id: Optional[str] = None

class TaskUpdate(BaseModel):
    content: Optional[str] = None
    owner: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None # 'open', 'in_progress', 'completed', 'overdue'

class TaskResponse(BaseModel):
    id: str
    workspace_id: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    meeting_id: Optional[str] = None
    meeting_title: Optional[str] = None
    node_id: Optional[str] = None
    content: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    status: str
    priority: str
    created_at: str

# Search schemas
class SearchResultItem(BaseModel):
    id: str
    type: str # 'meeting', 'customer', 'decision', 'requirement', 'deadline', 'risk', 'action_item', 'objection', 'task'
    title: str
    description: Optional[str] = None
    date: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]

# Alert schemas
class AlertNotification(BaseModel):
    id: str
    type: str # 'deadline', 'requirement_change', 'sentiment_drop', 'contradiction', 'risk_increase'
    title: str
    message: str
    reference_id: str # meeting_id or contradiction_id or task_id
    created_at: str

# WoW schemas
class RequirementDriftItem(BaseModel):
    date: str
    meeting_id: str
    meeting_title: str
    content: str
    speaker: str
    status: str # 'active', 'changed', 'superseded'
    drift_explanation: Optional[str] = None

class RequirementDriftResponse(BaseModel):
    customer_id: str
    customer_name: str
    timeline: List[RequirementDriftItem]

class CommitmentTrackerItem(BaseModel):
    id: str
    content: str
    speaker: str
    status: str
    deadline: Optional[str] = None
    owner: Optional[str] = None
    completed_date: Optional[str] = None

class CommitmentTrackerResponse(BaseModel):
    total: int
    completed: int
    pending: int
    completion_rate: float
    commitments: List[CommitmentTrackerItem]

class StakeholderScore(BaseModel):
    speaker: str
    influence_score: float # 0 to 100
    decision_count: int
    objection_count: int
    commitment_count: int

class StakeholderInfluenceResponse(BaseModel):
    stakeholders: List[StakeholderScore]

class CustomerTrustResponse(BaseModel):
    customer_id: str
    customer_name: str
    trust_score: float # 0 to 100
    explanation: str
    contradictions: List[ContradictionResponse]

class RiskRadarResponse(BaseModel):
    scope_creep: float # 0 to 100
    churn: float
    project_delay: float
    stakeholder_misalignment: float
