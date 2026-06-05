/** Shared TypeScript interfaces — mirror backend schemas */

export interface Customer {
  id: string;
  name: string;
  email?: string;
  industry?: string;
  relationship_health: number;
  created_at: string;
}

export interface Meeting {
  id: string;
  customer_id: string;
  title: string;
  meeting_date: string;
  status: "pending" | "processing" | "completed" | "failed";
  summary?: string;
  meeting_iq_score?: number;
  risk_level?: "low" | "medium" | "high";
}

export interface MeetingEntity {
  id: string;
  entity_type:
    | "requirement"
    | "commitment"
    | "deadline"
    | "objection"
    | "decision"
    | "concern";
  content: string;
  speaker?: string;
  status: "open" | "resolved" | "disputed";
}

export interface TruthVerificationResult {
  verdict: "verified" | "disputed" | "inconclusive";
  confidence: number;
  reasoning: string;
  evidence: EvidenceItem[];
}

export interface EvidenceItem {
  meeting_id: string;
  meeting_title: string;
  meeting_date: string;
  excerpt: string;
  speaker?: string;
  relevance_score: number;
}
