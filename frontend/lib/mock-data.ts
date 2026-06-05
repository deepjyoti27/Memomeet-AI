export const dashboardStats = {
  totalMeetings: 247,
  activeCustomers: 34,
  pendingFollowups: 12,
  upcomingDeadlines: 8,
  avgMeetingIQ: 78,
  riskAlerts: 3,
};

export const sentimentTrend = [
  { month: "Jan", score: 62 },
  { month: "Feb", score: 68 },
  { month: "Mar", score: 71 },
  { month: "Apr", score: 65 },
  { month: "May", score: 74 },
  { month: "Jun", score: 79 },
];

export const requirementChanges = [
  { month: "Jan", changes: 2 },
  { month: "Feb", changes: 4 },
  { month: "Mar", changes: 3 },
  { month: "Apr", changes: 7 },
  { month: "May", changes: 5 },
  { month: "Jun", changes: 3 },
];

export const meetingActivity = [
  { week: "W1", meetings: 8 },
  { week: "W2", meetings: 12 },
  { week: "W3", meetings: 10 },
  { week: "W4", meetings: 15 },
  { week: "W5", meetings: 11 },
  { week: "W6", meetings: 14 },
];

export const riskAlerts = [
  {
    id: "1",
    customer: "Acme Corp",
    risk: "Unresolved pricing objection from Q1",
    severity: "high" as const,
    date: "2026-06-01",
  },
  {
    id: "2",
    customer: "TechFlow Inc",
    risk: "CRM integration deadline at risk",
    severity: "medium" as const,
    date: "2026-05-28",
  },
  {
    id: "3",
    customer: "GlobalRetail",
    risk: "Requirement changed 3 times in 2 weeks",
    severity: "medium" as const,
    date: "2026-05-25",
  },
];

export const customers = [
  { id: "1", name: "Acme Corp", industry: "SaaS", health: 82 },
  { id: "2", name: "TechFlow Inc", industry: "FinTech", health: 71 },
  { id: "3", name: "GlobalRetail", industry: "E-commerce", health: 65 },
  { id: "4", name: "HealthPlus", industry: "Healthcare", health: 88 },
];

export const timelineEvents = [
  {
    id: "1",
    date: "2026-06-01",
    type: "meeting" as const,
    title: "Q2 Planning Review",
    description: "Discussed CRM integration timeline and API requirements.",
    customer: "Acme Corp",
  },
  {
    id: "2",
    date: "2026-05-22",
    type: "requirement" as const,
    title: "Requirement Change: API Rate Limits",
    description: "Increased from 1,000 to 5,000 requests/minute.",
    customer: "Acme Corp",
  },
  {
    id: "3",
    date: "2026-05-15",
    type: "commitment" as const,
    title: "Commitment: Beta Delivery",
    description: "Team committed to March 15 beta release for CRM module.",
    customer: "Acme Corp",
  },
  {
    id: "4",
    date: "2026-05-10",
    type: "objection" as const,
    title: "Pricing Objection Raised",
    description: "Customer concerned about enterprise tier pricing.",
    customer: "Acme Corp",
  },
  {
    id: "5",
    date: "2026-04-28",
    type: "decision" as const,
    title: "Decision: Salesforce Integration",
    description: "Agreed to prioritize Salesforce over HubSpot integration.",
    customer: "Acme Corp",
  },
  {
    id: "6",
    date: "2026-04-15",
    type: "meeting" as const,
    title: "Discovery Call",
    description: "Initial requirements gathering for CRM integration project.",
    customer: "Acme Corp",
  },
];

export const truthVerificationDemo = {
  query: "Did the customer discuss CRM integration?",
  verdict: "verified" as const,
  confidence: 94,
  summary:
    "CRM integration was discussed in 4 separate meetings between April and June 2026. The customer explicitly requested Salesforce integration with a target beta date of March 15.",
  evidence: [
    {
      meetingDate: "2026-06-01",
      meetingTitle: "Q2 Planning Review",
      excerpt:
        "Sarah (Acme): We need the CRM integration live before our Q3 campaign. Salesforce is non-negotiable.",
      speaker: "Sarah Chen",
      confidence: 96,
    },
    {
      meetingDate: "2026-04-28",
      meetingTitle: "Integration Strategy Call",
      excerpt:
        "John (Acme): Let's prioritize Salesforce integration over HubSpot. Our sales team runs entirely on Salesforce.",
      speaker: "John Martinez",
      confidence: 92,
    },
    {
      meetingDate: "2026-04-15",
      meetingTitle: "Discovery Call",
      excerpt:
        "Sarah: Our biggest pain point is manual data entry between our CRM and your platform. We need seamless sync.",
      speaker: "Sarah Chen",
      confidence: 89,
    },
  ],
};

export const meetingIQData = {
  overallScore: 78,
  riskScore: 32,
  effectiveness: {
    clarity: 82,
    commitments: 75,
    riskResolution: 68,
    followThrough: 80,
    engagement: 85,
  },
  unresolvedConcerns: [
    "Enterprise pricing model not finalized",
    "SSO integration timeline unclear",
    "Data migration scope undefined",
  ],
  missedFollowups: [
    { item: "Send revised SOW document", due: "2026-05-20", owner: "Alex" },
    { item: "Schedule technical deep-dive", due: "2026-05-25", owner: "Jordan" },
  ],
  recommendedActions: [
    "Schedule pricing review call within 48 hours",
    "Assign technical lead for SSO scoping",
    "Document data migration requirements in writing",
    "Send follow-up email with action items from last meeting",
  ],
};

export const assistantSuggestions = [
  "Prepare me for tomorrow's meeting with Acme Corp",
  "What were the customer's concerns about pricing?",
  "What commitments are still pending?",
  "Has the CRM integration deadline changed?",
  "Summarize our last 3 meetings with TechFlow",
];

export const assistantResponses: Record<string, string> = {
  default:
    "Based on your meeting memory, I can help you prepare for meetings, track commitments, and verify what was discussed. Try one of the suggested questions above.",
  "Prepare me for tomorrow's meeting with Acme Corp":
    "**Meeting Prep: Acme Corp**\n\n**Key Context:**\n- CRM Salesforce integration is their top priority\n- Beta deadline discussed: March 15 (may need reconfirmation)\n- Open concern: Enterprise pricing not finalized\n\n**Pending Commitments (Your Team):**\n- Send revised SOW document (overdue)\n- Schedule technical deep-dive for SSO\n\n**Likely Discussion Topics:**\n1. API rate limit increase (recently changed to 5,000/min)\n2. Q3 campaign timeline dependencies\n3. Data migration scope\n\n**Recommended Approach:** Lead with pricing clarity and confirm the CRM timeline.",
  "What were the customer's concerns about pricing?":
    "Acme Corp raised pricing concerns in the **May 10, 2026** meeting. Sarah Chen stated the enterprise tier pricing felt \"disproportionate to the value for mid-market teams.\" This objection remains **unresolved** — no follow-up pricing review has been documented.",
  "What commitments are still pending?":
    "**Pending Commitments:**\n\n| Owner | Commitment | Due | Status |\n|-------|-----------|-----|--------|\n| Alex | Send revised SOW document | May 20 | Overdue |\n| Jordan | Schedule technical deep-dive | May 25 | Overdue |\n| Your Team | CRM beta delivery | Mar 15 | At Risk |\n| Acme Corp | Provide data migration specs | May 30 | Waiting |",
};

export const processedMeetingOutput = {
  summary:
    "The team discussed Q2 planning priorities with Acme Corp, focusing on CRM Salesforce integration timeline. Key decisions included increasing API rate limits and confirming the Q3 campaign dependency on the integration go-live date.",
  actionItems: [
    { task: "Send revised SOW with updated pricing tiers", owner: "Alex", due: "2026-06-08" },
    { task: "Schedule SSO technical deep-dive", owner: "Jordan", due: "2026-06-10" },
    { task: "Provide Salesforce sandbox credentials", owner: "Sarah (Acme)", due: "2026-06-12" },
  ],
  decisions: [
    "Prioritize Salesforce integration over HubSpot",
    "Increase API rate limits to 5,000 requests/minute",
    "Target Q3 campaign launch contingent on CRM go-live",
  ],
  deadlines: [
    { item: "CRM Beta Release", date: "2026-03-15", status: "at-risk" },
    { item: "SOW Delivery", date: "2026-06-08", status: "pending" },
    { item: "Q3 Campaign Launch", date: "2026-07-01", status: "upcoming" },
  ],
};
