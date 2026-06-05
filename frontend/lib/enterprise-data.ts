export const company = {
  name: "MemoMeet AI",
  tagline: "Enterprise Truth & Commitment Intelligence",
  description:
    "The system of record for what was promised, decided, and agreed — across every customer conversation.",
};

export const dashboardMetrics = {
  commitmentsTracked: 1847,
  commitmentsDelta: 12.4,
  truthQueries: 342,
  truthQueriesDelta: 28,
  driftAlerts: 23,
  driftAlertsDelta: -8,
  atRiskAccounts: 7,
  avgMeetingIQ: 81,
  disputedClaimsResolved: 94,
  memoryRetention: "99.7%",
};

export const customers = [
  {
    id: "acme",
    name: "Acme Corporation",
    industry: "Enterprise SaaS",
    arr: "$2.4M",
    health: 72,
    risk: "elevated",
    meetings: 47,
    commitments: 128,
    owner: "Sarah Mitchell",
  },
  {
    id: "techflow",
    name: "TechFlow Inc",
    industry: "FinTech",
    arr: "$890K",
    health: 88,
    risk: "low",
    meetings: 23,
    commitments: 64,
    owner: "James Chen",
  },
  {
    id: "globalretail",
    name: "GlobalRetail Group",
    industry: "E-Commerce",
    arr: "$1.6M",
    health: 61,
    risk: "critical",
    meetings: 31,
    commitments: 89,
    owner: "Priya Sharma",
  },
  {
    id: "healthplus",
    name: "HealthPlus Systems",
    industry: "Healthcare",
    arr: "$3.1M",
    health: 91,
    risk: "low",
    meetings: 52,
    commitments: 156,
    owner: "Marcus Webb",
  },
];

export const commitments = [
  {
    id: "c1",
    type: "Requirement",
    statement: "CRM integration with Salesforce must be live by September 30",
    owner: "Customer",
    speaker: "Sarah Chen",
    customer: "Acme Corporation",
    meetingDate: "2026-03-15",
    meetingTitle: "Q1 Integration Planning",
    confidence: 97,
    status: "active",
    deadline: "2026-09-30",
  },
  {
    id: "c2",
    type: "Commitment",
    statement: "We will deliver revised enterprise pricing by end of week",
    owner: "Internal",
    speaker: "Alex Rivera",
    customer: "Acme Corporation",
    meetingDate: "2026-05-10",
    meetingTitle: "Pricing Review Call",
    confidence: 99,
    status: "overdue",
    deadline: "2026-05-17",
  },
  {
    id: "c3",
    type: "Approval",
    statement: "Customer approved Phase 2 scope including SSO and audit logs",
    owner: "Customer",
    speaker: "John Martinez",
    customer: "Acme Corporation",
    meetingDate: "2026-04-22",
    meetingTitle: "Scope Sign-off",
    confidence: 96,
    status: "verified",
    deadline: null,
  },
  {
    id: "c4",
    type: "Objection",
    statement: "Enterprise tier pricing is disproportionate for mid-market teams",
    owner: "Customer",
    speaker: "Sarah Chen",
    customer: "Acme Corporation",
    meetingDate: "2026-05-10",
    meetingTitle: "Pricing Review Call",
    confidence: 94,
    status: "unresolved",
    deadline: null,
  },
  {
    id: "c5",
    type: "Requirement",
    statement: "Need Android app with offline sync capability",
    owner: "Customer",
    speaker: "David Park",
    customer: "GlobalRetail Group",
    meetingDate: "2026-01-20",
    meetingTitle: "Mobile Strategy Kickoff",
    confidence: 98,
    status: "superseded",
    deadline: "2026-08-01",
  },
  {
    id: "c6",
    type: "Requirement",
    statement: "Android + iOS + Web platform with unified inventory sync",
    owner: "Customer",
    speaker: "David Park",
    customer: "GlobalRetail Group",
    meetingDate: "2026-05-28",
    meetingTitle: "Scope Expansion Review",
    confidence: 97,
    status: "active",
    deadline: "2026-11-15",
  },
  {
    id: "c7",
    type: "Deadline",
    statement: "Beta release targeted for March 15",
    owner: "Internal",
    speaker: "Jordan Lee",
    customer: "Acme Corporation",
    meetingDate: "2026-03-01",
    meetingTitle: "Sprint Planning",
    confidence: 95,
    status: "at-risk",
    deadline: "2026-03-15",
  },
  {
    id: "c8",
    type: "Commitment",
    statement: "Customer will provide Salesforce sandbox credentials within 5 business days",
    owner: "Customer",
    speaker: "Sarah Chen",
    customer: "Acme Corporation",
    meetingDate: "2026-06-01",
    meetingTitle: "Q2 Planning Review",
    confidence: 93,
    status: "pending",
    deadline: "2026-06-08",
  },
];

export const truthQueries = [
  {
    id: "t1",
    query: "Did customer ever approve pricing?",
    verdict: "partial",
    confidence: 78,
    customer: "Acme Corporation",
    timestamp: "2026-06-04T14:32:00Z",
  },
  {
    id: "t2",
    query: "Was CRM integration discussed before April?",
    verdict: "verified",
    confidence: 97,
    customer: "Acme Corporation",
    timestamp: "2026-06-03T09:15:00Z",
  },
];

export const truthEngineResult = {
  query: "Did customer ever approve pricing?",
  customer: "Acme Corporation",
  verdict: "partial" as const,
  confidence: 78,
  summary:
    "Pricing was discussed across 6 meetings but formal enterprise pricing approval was never explicitly granted. Phase 2 scope was approved; pricing structure remains contested.",
  evidence: [
    {
      statement:
        "The Phase 2 numbers look reasonable — let's proceed with scope as discussed.",
      speaker: "John Martinez",
      role: "VP Engineering, Acme",
      meetingDate: "2026-04-22",
      meetingTitle: "Scope Sign-off",
      timestamp: "00:34:12",
      confidence: 91,
      transcriptId: "MTG-2026-0422-001",
    },
    {
      statement:
        "I can't sign off on enterprise pricing until we see the mid-market tier breakdown.",
      speaker: "Sarah Chen",
      role: "CFO, Acme",
      meetingDate: "2026-05-10",
      meetingTitle: "Pricing Review Call",
      timestamp: "00:18:45",
      confidence: 97,
      transcriptId: "MTG-2026-0510-003",
    },
    {
      statement:
        "We need revised pricing by Friday or this deal stalls.",
      speaker: "Sarah Chen",
      role: "CFO, Acme",
      meetingDate: "2026-05-10",
      meetingTitle: "Pricing Review Call",
      timestamp: "00:42:03",
      confidence: 99,
      transcriptId: "MTG-2026-0510-003",
    },
  ],
};

export const requirementDrift = {
  customer: "GlobalRetail Group",
  meetings: [
    { id: 1, date: "2026-01-20", title: "Mobile Strategy Kickoff", scope: "Android app with offline sync" },
    { id: 2, date: "2026-02-14", title: "Technical Review", scope: "Android app + push notifications" },
    { id: 3, date: "2026-03-22", title: "Q1 Retrospective", scope: "Android app + admin dashboard" },
    { id: 4, date: "2026-04-18", title: "Stakeholder Sync", scope: "Android + basic web portal" },
    { id: 5, date: "2026-05-28", title: "Scope Expansion Review", scope: "Android + iOS + Web with unified inventory sync" },
  ],
  driftScore: 84,
  expansionRate: "340%",
  contradictions: [
    {
      earlier: "Android-only MVP by August",
      later: "Full cross-platform by November",
      meetingA: "2026-01-20",
      meetingB: "2026-05-28",
    },
  ],
  newRequirements: [
    "iOS native application",
    "Web platform parity",
    "Unified real-time inventory sync",
    "Offline mode across all platforms",
  ],
  removedRequirements: [],
};

export const customerDNA = {
  customer: "Acme Corporation",
  profile: {
    priorities: ["CRM Integration", "Enterprise Security", "API Scalability", "SSO"],
    objections: [
      { topic: "Enterprise Pricing", frequency: 4, lastRaised: "2026-05-10", severity: "high" },
      { topic: "Implementation Timeline", frequency: 2, lastRaised: "2026-04-15", severity: "medium" },
      { topic: "Data Residency", frequency: 1, lastRaised: "2026-03-22", severity: "low" },
    ],
    buyingSignals: [
      { signal: "Requested sandbox environment", date: "2026-05-28", strength: "strong" },
      { signal: "Introduced VP Engineering to call", date: "2026-04-22", strength: "strong" },
      { signal: "Asked about multi-year contract terms", date: "2026-06-01", strength: "moderate" },
    ],
    communicationStyle: "Direct, data-driven, prefers written confirmations",
    featureRequests: [
      { feature: "Salesforce Bi-directional Sync", count: 8 },
      { feature: "Custom Audit Logs", count: 5 },
      { feature: "Role-based Access Control", count: 4 },
      { feature: "Webhook Event Streaming", count: 3 },
    ],
    sentimentTrend: [
      { month: "Jan", score: 62 },
      { month: "Feb", score: 68 },
      { month: "Mar", score: 71 },
      { month: "Apr", score: 74 },
      { month: "May", score: 58 },
      { month: "Jun", score: 65 },
    ],
    relationshipHealth: 72,
    decisionMakers: ["Sarah Chen (CFO)", "John Martinez (VP Eng)", "Alex Kim (IT Director)"],
    commitmentScore: {
      overall: 65,
      dimensions: [
        {
          label: "CRM Integration",
          score: 95,
          status: "strong" as const,
          evidence: "Discussed in 4 meetings with explicit September deadline",
        },
        {
          label: "Budget Approval",
          score: 40,
          status: "weak" as const,
          evidence: "Pricing objection unresolved — no formal sign-off",
        },
        {
          label: "Timeline Agreement",
          score: 60,
          status: "hesitant" as const,
          evidence: "Customer expressed hesitation on delivery dates",
        },
      ],
      warning: {
        title: "Timeline Hesitation Detected",
        message:
          "Customer showed hesitation on timeline. Multiple meetings reference conflicting delivery dates. Recommend written confirmation before next milestone.",
        severity: "high" as const,
        source: "Q2 Planning Review · 2026-06-01",
      },
    },
  },
};

export const trustTimeline = [
  { id: "1", date: "2026-06-01", type: "requirement_added", title: "Salesforce sandbox credentials due", customer: "Acme Corporation", impact: "medium" },
  { id: "2", date: "2026-05-28", type: "requirement_added", title: "Cross-platform scope expansion", customer: "GlobalRetail Group", impact: "high" },
  { id: "3", date: "2026-05-10", type: "objection", title: "Enterprise pricing objection raised", customer: "Acme Corporation", impact: "critical" },
  { id: "4", date: "2026-05-10", type: "commitment", title: "Revised pricing due end of week", customer: "Acme Corporation", impact: "high" },
  { id: "5", date: "2026-04-22", type: "approval", title: "Phase 2 scope approved", customer: "Acme Corporation", impact: "medium" },
  { id: "6", date: "2026-04-22", type: "decision", title: "Prioritize Salesforce over HubSpot", customer: "Acme Corporation", impact: "medium" },
  { id: "7", date: "2026-03-15", type: "requirement_added", title: "CRM integration by September 30", customer: "Acme Corporation", impact: "high" },
  { id: "8", date: "2026-03-01", type: "deadline", title: "Beta release March 15", customer: "Acme Corporation", impact: "high" },
  { id: "9", date: "2026-02-14", type: "risk", title: "Timeline slip risk identified", customer: "GlobalRetail Group", impact: "medium" },
  { id: "10", date: "2026-01-20", type: "requirement_added", title: "Android app with offline sync", customer: "GlobalRetail Group", impact: "low" },
];

export const disputeCase = {
  claim: "We never requested that feature.",
  feature: "SSO with SAML 2.0 and audit log export",
  customer: "Acme Corporation",
  verdict: "disputed" as const,
  confidence: 96,
  evidence: [
    {
      statement: "We absolutely need SSO — SAML 2.0 is non-negotiable for our security review.",
      speaker: "Alex Kim",
      meetingDate: "2026-04-22",
      meetingTitle: "Scope Sign-off",
      timestamp: "00:22:18",
      confidence: 98,
    },
    {
      statement: "Audit log export needs to cover 90 days minimum for compliance.",
      speaker: "John Martinez",
      meetingDate: "2026-04-22",
      meetingTitle: "Scope Sign-off",
      timestamp: "00:28:44",
      confidence: 97,
    },
  ],
};

export const riskRadar = {
  overallRisk: 68,
  categories: [
    { name: "Forgotten Promises", score: 72, count: 5, trend: "up" },
    { name: "Missed Deadlines", score: 81, count: 3, trend: "up" },
    { name: "Contradictory Statements", score: 45, count: 2, trend: "stable" },
    { name: "Scope Drift", score: 84, count: 4, trend: "up" },
    { name: "Unresolved Objections", score: 76, count: 6, trend: "up" },
  ],
  highRiskCustomers: [
    { customer: "GlobalRetail Group", risk: 91, primaryThreat: "340% scope expansion untracked", commitments: 12 },
    { customer: "Acme Corporation", risk: 78, primaryThreat: "Overdue pricing commitment + CRM deadline", commitments: 8 },
    { customer: "TechFlow Inc", risk: 34, primaryThreat: "Minor follow-up gaps", commitments: 2 },
  ],
  alerts: [
    { id: "a1", severity: "critical", title: "Pricing commitment 19 days overdue", customer: "Acme Corporation", daysOpen: 19 },
    { id: "a2", severity: "critical", title: "Scope expanded 340% without change order", customer: "GlobalRetail Group", daysOpen: 8 },
    { id: "a3", severity: "high", title: "CRM beta deadline missed — no resolution logged", customer: "Acme Corporation", daysOpen: 82 },
    { id: "a4", severity: "high", title: "Contradictory timeline statements detected", customer: "Acme Corporation", daysOpen: 14 },
    { id: "a5", severity: "medium", title: "Sandbox credentials pending from customer", customer: "Acme Corporation", daysOpen: 4 },
  ],
};

export const meetingIQ = {
  recentMeetings: [
    { title: "Q2 Planning Review", customer: "Acme Corporation", date: "2026-06-01", iq: 78, clarity: 82, commitment: 75, risk: 68, decision: 80, engagement: 85 },
    { title: "Scope Expansion Review", customer: "GlobalRetail Group", date: "2026-05-28", iq: 62, clarity: 58, commitment: 55, risk: 88, decision: 60, engagement: 72 },
    { title: "Pricing Review Call", customer: "Acme Corporation", date: "2026-05-10", iq: 71, clarity: 70, commitment: 65, risk: 82, decision: 68, engagement: 78 },
  ],
};

export const activityFeed = [
  { time: "2m ago", event: "Truth query resolved", detail: "CRM integration timeline — 97% confidence", type: "truth" },
  { time: "18m ago", event: "Drift detected", detail: "GlobalRetail scope +340% expansion", type: "drift" },
  { time: "1h ago", event: "Commitment overdue", detail: "Revised pricing — Acme Corporation", type: "risk" },
  { time: "3h ago", event: "Meeting processed", detail: "Q2 Planning Review — IQ 78", type: "meeting" },
  { time: "5h ago", event: "Dispute evidence generated", detail: "SSO feature request — 96% confidence", type: "dispute" },
];
