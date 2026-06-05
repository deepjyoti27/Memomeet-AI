import {
  Brain,
  GitCompare,
  LineChart,
  Mail,
  Mic,
  ShieldCheck,
  Upload,
  Users,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const features = [
  {
    icon: Mic,
    title: "Meeting Recording & Processing",
    description:
      "Upload audio or transcripts. AI identifies speakers and extracts structured insights automatically.",
  },
  {
    icon: Brain,
    title: "AI Meeting Memory",
    description:
      "Hindsight Memory stores requirements, commitments, deadlines, and objections across every customer.",
  },
  {
    icon: Users,
    title: "Customer Intelligence Timeline",
    description:
      "Visualize how customer requirements evolved across months of meetings and decisions.",
  },
  {
    icon: ShieldCheck,
    title: "Truth Verification Engine",
    description:
      "When customers claim something wasn't discussed, find evidence with meeting excerpts and confidence scores.",
  },
  {
    icon: GitCompare,
    title: "Meeting Comparison",
    description:
      "Detect changed requirements, contradictory statements, and emerging risks across meetings.",
  },
  {
    icon: Mail,
    title: "AI Follow-Up Generator",
    description:
      "Auto-generate follow-up emails, action items, and next meeting agendas from meeting memory.",
  },
  {
    icon: LineChart,
    title: "Meeting IQ Score",
    description:
      "Score meetings 0–100 on effectiveness, predict project risk, and get recommended next actions.",
  },
  {
    icon: Upload,
    title: "Enterprise Dashboard",
    description:
      "Track sentiment trends, common objections, feature requests, and relationship health scores.",
  },
];

export function Features() {
  return (
    <section id="features" className="py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Everything Your Team Needs to{" "}
            <span className="gradient-text">Never Forget</span>
          </h2>
          <p className="mt-4 text-muted-foreground">
            From recording to verification — a complete meeting intelligence
            platform built for enterprise teams.
          </p>
        </div>

        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map(({ icon: Icon, title, description }) => (
            <Card
              key={title}
              className="group transition-all hover:border-primary/30 hover:shadow-lg"
            >
              <CardHeader className="pb-3">
                <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-brand-subtle text-primary transition-colors group-hover:bg-gradient-brand group-hover:text-white">
                  <Icon className="h-5 w-5" />
                </div>
                <CardTitle className="text-base">{title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
