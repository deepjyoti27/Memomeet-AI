import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  Dna,
  GitCompare,
  Hexagon,
  Radar,
  Shield,
  GitBranch,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const features = [
  {
    icon: BookOpen,
    name: "Commitment Ledger™",
    desc: "Every promise, requirement, deadline, and approval — extracted and immutable.",
  },
  {
    icon: Shield,
    name: "Business Truth Engine™",
    desc: "Ask any question. Get exact statements, dates, speakers, and evidence scores.",
  },
  {
    icon: GitCompare,
    name: "Requirement Drift Detection™",
    desc: "Automatically detect scope expansion and contradictory statements across meetings.",
  },
  {
    icon: Dna,
    name: "Customer DNA™",
    desc: "Permanent memory profiles — priorities, objections, buying signals, sentiment.",
  },
  {
    icon: GitBranch,
    name: "Trust Timeline™",
    desc: "Visual audit trail of requirements added, removed, decided, and approved.",
  },
  {
    icon: Shield,
    name: "Dispute Resolution Mode™",
    desc: "When customers deny requests — surface meeting evidence with timestamps.",
  },
  {
    icon: Radar,
    name: "Commitment Risk Radar™",
    desc: "Predict forgotten promises, missed deadlines, and high-risk accounts.",
  },
  {
    icon: Hexagon,
    name: "Meeting IQ™",
    desc: "Score clarity, commitment strength, risk, and decision quality per meeting.",
  },
];

const stats = [
  { value: "$4.2M", label: "Avg. revenue at risk per enterprise deal" },
  { value: "73%", label: "Of disputes lack documented evidence" },
  { value: "340%", label: "Typical undetected scope expansion" },
  { value: "94%", label: "Dispute resolution rate with MemoMeet" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#09090b] text-foreground">
      <div className="enterprise-grid fixed inset-0 opacity-40" />
      <div className="relative">
        {/* Nav */}
        <nav className="fixed top-0 z-50 w-full border-b border-white/[0.06] bg-[#09090b]/80 backdrop-blur-xl">
          <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
            <div className="flex items-center gap-2.5">
              <div className="flex h-7 w-7 items-center justify-center rounded-md bg-gradient-to-br from-blue-500 to-violet-600">
                <Hexagon className="h-3.5 w-3.5 text-white" />
              </div>
              <span className="text-sm font-semibold">MemoMeet AI</span>
            </div>
            <div className="hidden items-center gap-8 md:flex">
              <a href="#platform" className="text-[13px] text-muted-foreground hover:text-foreground">
                Platform
              </a>
              <a href="#problem" className="text-[13px] text-muted-foreground hover:text-foreground">
                Problem
              </a>
              <a href="#features" className="text-[13px] text-muted-foreground hover:text-foreground">
                Features
              </a>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" asChild className="text-[13px]">
                <Link href="/dashboard">Sign in</Link>
              </Button>
              <Button
                size="sm"
                asChild
                className="bg-white text-black hover:bg-white/90 text-[13px]"
              >
                <Link href="/dashboard">
                  Open Platform
                  <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                </Link>
              </Button>
            </div>
          </div>
        </nav>

        {/* Hero */}
        <section className="relative px-6 pb-24 pt-32">
          <div className="absolute left-1/2 top-20 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-blue-500/5 blur-3xl" />
          <div className="relative mx-auto max-w-4xl text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 py-1 text-[11px] text-muted-foreground">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Enterprise Truth & Commitment Intelligence
            </div>
            <h1 className="text-4xl font-semibold leading-[1.1] tracking-tight sm:text-6xl lg:text-7xl">
              The system of record for{" "}
              <span className="gradient-text">what was promised</span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
              Companies lose millions when commitments vanish, requirements
              drift, and customers deny what was agreed. MemoMeet is the
              intelligence layer that remembers everything.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Button
                size="lg"
                asChild
                className="h-11 bg-white px-8 text-black hover:bg-white/90"
              >
                <Link href="/dashboard">
                  Enter Platform
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                asChild
                className="h-11 border-white/[0.1] bg-transparent hover:bg-white/[0.04]"
              >
                <Link href="/truth-engine">Try Truth Engine</Link>
              </Button>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section id="problem" className="border-y border-white/[0.06] bg-white/[0.01] px-6 py-16">
          <div className="mx-auto grid max-w-5xl gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map(({ value, label }) => (
              <div key={label} className="text-center">
                <p className="text-3xl font-semibold tracking-tight">{value}</p>
                <p className="mt-2 text-[13px] text-muted-foreground">{label}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Features */}
        <section id="features" className="px-6 py-24">
          <div className="mx-auto max-w-6xl">
            <div className="mb-16 max-w-2xl">
              <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-400">
                Platform
              </p>
              <h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">
                Eight intelligence systems.
                <br />
                One source of truth.
              </h2>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {features.map(({ icon: Icon, name, desc }) => (
                <div
                  key={name}
                  className="enterprise-card-hover group p-5"
                >
                  <div className="mb-4 flex h-9 w-9 items-center justify-center rounded-md border border-white/[0.06] bg-white/[0.03] text-muted-foreground transition-colors group-hover:border-blue-500/30 group-hover:text-blue-400">
                    <Icon className="h-4 w-4" />
                  </div>
                  <h3 className="text-[13px] font-semibold">{name}</h3>
                  <p className="mt-2 text-[12px] leading-relaxed text-muted-foreground">
                    {desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section id="platform" className="px-6 pb-24">
          <div className="mx-auto max-w-3xl rounded-xl border border-white/[0.08] bg-gradient-to-b from-white/[0.04] to-transparent p-12 text-center">
            <h2 className="text-2xl font-semibold sm:text-3xl">
              Stop losing deals to forgotten commitments
            </h2>
            <p className="mt-3 text-muted-foreground">
              Join enterprise teams using MemoMeet as their commitment system
              of record.
            </p>
            <Button
              size="lg"
              asChild
              className="mt-8 h-11 bg-white px-8 text-black hover:bg-white/90"
            >
              <Link href="/dashboard">
                Open MemoMeet Platform
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </section>

        <footer className="border-t border-white/[0.06] px-6 py-8">
          <div className="mx-auto flex max-w-6xl items-center justify-between">
            <p className="text-[12px] text-muted-foreground">
              © 2026 MemoMeet AI. Enterprise Truth & Commitment Intelligence.
            </p>
            <p className="font-mono text-[11px] text-muted-foreground">
              v2.0.0-enterprise
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
}
