"use client";

import Link from "next/link";
import { AlertTriangle, Radar, Shield } from "lucide-react";
import { PageHeader } from "@/components/enterprise/page-header";
import { StatusBadge } from "@/components/enterprise/status-badge";
import { EvidenceCard } from "@/components/enterprise/evidence-card";
import { Button } from "@/components/ui/button";
import { riskRadar, disputeCase } from "@/lib/enterprise-data";

export default function RiskRadarPage() {
  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Commitment Risk Radar™"
        title="Risk Radar"
        description="Predict forgotten promises, missed deadlines, contradictory statements, and high-risk accounts."
      />

      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="intel-panel border-red-500/20 sm:col-span-2 lg:col-span-1">
          <div className="flex items-center gap-3">
            <Radar className="h-8 w-8 text-red-400" />
            <div>
              <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                Portfolio Risk Index
              </p>
              <p className="font-mono text-4xl font-semibold text-red-400">
                {riskRadar.overallRisk}
              </p>
            </div>
          </div>
        </div>
        {riskRadar.categories.slice(0, 2).map((cat) => (
          <div key={cat.name} className="intel-panel">
            <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
              {cat.name}
            </p>
            <div className="mt-2 flex items-end justify-between">
              <p className="font-mono text-2xl font-semibold">{cat.score}</p>
              <div className="text-right">
                <p className="text-[11px] text-muted-foreground">
                  {cat.count} active
                </p>
                <StatusBadge
                  status={cat.trend === "up" ? "critical" : "pending"}
                />
              </div>
            </div>
            <div className="mt-3 h-1 overflow-hidden rounded-full bg-white/[0.06]">
              <div
                className="h-full rounded-full bg-gradient-to-r from-amber-500 to-red-500"
                style={{ width: `${cat.score}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mb-6 grid gap-4 lg:grid-cols-3">
        {riskRadar.categories.slice(2).map((cat) => (
          <div key={cat.name} className="intel-panel">
            <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
              {cat.name}
            </p>
            <p className="mt-1 font-mono text-2xl font-semibold">{cat.score}</p>
            <p className="text-[11px] text-muted-foreground">
              {cat.count} instances
            </p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            High-Risk Accounts
          </p>
          <div className="space-y-2">
            {riskRadar.highRiskCustomers.map((c, i) => (
              <div
                key={i}
                className="enterprise-card-hover flex items-center justify-between p-4"
              >
                <div>
                  <p className="text-[13px] font-medium">{c.customer}</p>
                  <p className="mt-0.5 text-[11px] text-muted-foreground">
                    {c.primaryThreat}
                  </p>
                  <p className="mt-1 text-[10px] text-muted-foreground">
                    {c.commitments} open commitments
                  </p>
                </div>
                <div className="text-right">
                  <p
                    className={`font-mono text-2xl font-semibold ${
                      c.risk >= 80
                        ? "text-red-400"
                        : c.risk >= 50
                          ? "text-amber-400"
                          : "text-emerald-400"
                    }`}
                  >
                    {c.risk}
                  </p>
                  <p className="text-[10px] text-muted-foreground">risk</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Active Alerts
          </p>
          <div className="space-y-2">
            {riskRadar.alerts.map((alert) => (
              <div
                key={alert.id}
                className="flex items-start gap-3 rounded-md border border-white/[0.04] bg-white/[0.02] p-3"
              >
                <AlertTriangle
                  className={`mt-0.5 h-4 w-4 shrink-0 ${
                    alert.severity === "critical"
                      ? "text-red-400"
                      : "text-amber-400"
                  }`}
                />
                <div className="flex-1">
                  <p className="text-[12px] font-medium">{alert.title}</p>
                  <p className="text-[11px] text-muted-foreground">
                    {alert.customer} · {alert.daysOpen} days open
                  </p>
                </div>
                <StatusBadge status={alert.severity} />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Dispute Resolution Mode */}
      <div className="mt-8">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-blue-400" />
            <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Dispute Resolution Mode™
            </p>
          </div>
          <Button variant="ghost" size="sm" asChild className="h-7 text-[11px]">
            <Link href="/truth-engine">Open Truth Engine →</Link>
          </Button>
        </div>

        <div className="intel-panel border-blue-500/20">
          <div className="mb-4 flex items-start justify-between">
            <div>
              <p className="text-[11px] uppercase tracking-wider text-red-400">
                Customer Claim
              </p>
              <p className="mt-1 text-[15px] font-medium">
                &ldquo;{disputeCase.claim}&rdquo;
              </p>
              <p className="mt-2 text-[12px] text-muted-foreground">
                Feature disputed: {disputeCase.feature}
              </p>
            </div>
            <div className="text-right">
              <p className="text-[11px] uppercase tracking-wider text-emerald-400">
                Evidence Found
              </p>
              <p className="font-mono text-2xl font-semibold text-emerald-400">
                {disputeCase.confidence}%
              </p>
            </div>
          </div>
          <div className="space-y-3">
            {disputeCase.evidence.map((e, i) => (
              <EvidenceCard
                key={i}
                statement={e.statement}
                speaker={e.speaker}
                meetingDate={e.meetingDate}
                meetingTitle={e.meetingTitle}
                timestamp={e.timestamp}
                confidence={e.confidence}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
