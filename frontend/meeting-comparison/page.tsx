"use client";

import { AlertTriangle, ArrowRight, GitCompare } from "lucide-react";
import { PageHeader } from "@/components/enterprise/page-header";
import { ConfidenceBadge } from "@/components/enterprise/confidence-badge";
import { requirementDrift } from "@/lib/enterprise-data";

export default function MeetingComparisonPage() {
  const drift = requirementDrift;

  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Requirement Drift Detection™"
        title="Meeting Comparison"
        description="Compare meetings over time. Detect scope expansion, contradictions, and requirement evolution automatically."
      />

      <div className="mb-6 grid gap-4 sm:grid-cols-3">
        <div className="intel-panel border-red-500/20 stat-glow">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Drift Score
          </p>
          <p className="mt-1 font-mono text-4xl font-semibold text-red-400">
            {drift.driftScore}
          </p>
          <p className="mt-1 text-[11px] text-muted-foreground">
            Critical scope expansion detected
          </p>
        </div>
        <div className="intel-panel">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Scope Expansion
          </p>
          <p className="mt-1 font-mono text-4xl font-semibold text-amber-400">
            {drift.expansionRate}
          </p>
          <p className="mt-1 text-[11px] text-muted-foreground">
            Meeting 1 → Meeting 5
          </p>
        </div>
        <div className="intel-panel">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Account
          </p>
          <p className="mt-1 text-lg font-semibold">{drift.customer}</p>
          <p className="mt-1 text-[11px] text-muted-foreground">
            {drift.meetings.length} meetings analyzed
          </p>
        </div>
      </div>

      {/* Scope evolution */}
      <div className="intel-panel mb-6">
        <div className="mb-4 flex items-center gap-2">
          <GitCompare className="h-4 w-4 text-blue-400" />
          <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Scope Evolution
          </p>
        </div>
        <div className="space-y-3">
          {drift.meetings.map((m, i) => (
            <div key={m.id} className="flex items-start gap-4">
              <div className="flex flex-col items-center">
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-full font-mono text-[11px] font-semibold ${
                    i === drift.meetings.length - 1
                      ? "bg-red-500/20 text-red-400 ring-2 ring-red-500/30"
                      : "bg-white/[0.06] text-muted-foreground"
                  }`}
                >
                  {m.id}
                </div>
                {i < drift.meetings.length - 1 && (
                  <div className="mt-1 h-6 w-px bg-white/[0.08]" />
                )}
              </div>
              <div className="flex-1 rounded-md border border-white/[0.04] bg-white/[0.02] p-3">
                <div className="flex items-center justify-between">
                  <p className="text-[12px] font-medium">{m.title}</p>
                  <span className="font-mono text-[10px] text-muted-foreground">
                    {m.date}
                  </span>
                </div>
                <p className="mt-1 text-[12px] text-muted-foreground">
                  {m.scope}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            New Requirements Detected
          </p>
          <div className="space-y-2">
            {drift.newRequirements.map((req, i) => (
              <div
                key={i}
                className="flex items-center gap-2 rounded-md border border-red-500/10 bg-red-500/5 p-3"
              >
                <AlertTriangle className="h-3.5 w-3.5 shrink-0 text-red-400" />
                <p className="text-[12px]">{req}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Contradictions
          </p>
          {drift.contradictions.map((c, i) => (
            <div
              key={i}
              className="space-y-3 rounded-md border border-amber-500/10 bg-amber-500/5 p-4"
            >
              <div>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
                  Meeting {c.meetingA}
                </p>
                <p className="mt-1 text-[12px]">{c.earlier}</p>
              </div>
              <ArrowRight className="h-4 w-4 text-amber-400" />
              <div>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
                  Meeting {c.meetingB}
                </p>
                <p className="mt-1 text-[12px] font-medium">{c.later}</p>
              </div>
              <ConfidenceBadge score={91} size="sm" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
