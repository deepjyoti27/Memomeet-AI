"use client";

import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { PageHeader } from "@/components/enterprise/page-header";
import { StatusBadge } from "@/components/enterprise/status-badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { CustomerCommitmentScore } from "@/components/enterprise/customer-commitment-score";
import { customers, customerDNA } from "@/lib/enterprise-data";

export default function CustomerDNAPage() {
  const dna = customerDNA.profile;

  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Customer DNA™"
        title="Customer DNA"
        description="Permanent memory profile — priorities, objections, buying signals, and communication patterns."
      >
        <Select defaultValue="acme">
          <SelectTrigger className="w-48 border-white/[0.06] bg-white/[0.03]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {customers.map((c) => (
              <SelectItem key={c.id} value={c.id}>
                {c.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </PageHeader>

      <div className="mb-6">
        <CustomerCommitmentScore
          data={dna.commitmentScore}
          customer={customerDNA.customer}
        />
      </div>

      <div className="mb-6 grid gap-4 sm:grid-cols-4">
        <div className="intel-panel text-center">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Relationship Health
          </p>
          <p className="mt-1 font-mono text-3xl font-semibold text-amber-400">
            {dna.relationshipHealth}
          </p>
        </div>
        <div className="intel-panel text-center">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Open Objections
          </p>
          <p className="mt-1 font-mono text-3xl font-semibold">
            {dna.objections.length}
          </p>
        </div>
        <div className="intel-panel text-center">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Buying Signals
          </p>
          <p className="mt-1 font-mono text-3xl font-semibold text-emerald-400">
            {dna.buyingSignals.length}
          </p>
        </div>
        <div className="intel-panel text-center">
          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
            Decision Makers
          </p>
          <p className="mt-1 font-mono text-3xl font-semibold">
            {dna.decisionMakers.length}
          </p>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Priorities
          </p>
          <div className="flex flex-wrap gap-2">
            {dna.priorities.map((p) => (
              <span
                key={p}
                className="rounded-md border border-blue-500/20 bg-blue-500/10 px-2.5 py-1 text-[12px] text-blue-300"
              >
                {p}
              </span>
            ))}
          </div>
          <p className="mt-6 mb-3 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Communication Style
          </p>
          <p className="text-[13px] text-muted-foreground">
            {dna.communicationStyle}
          </p>
          <p className="mt-6 mb-3 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Decision Makers
          </p>
          <div className="space-y-1">
            {dna.decisionMakers.map((dm) => (
              <p key={dm} className="font-mono text-[12px]">
                {dm}
              </p>
            ))}
          </div>
        </div>

        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Objection Patterns
          </p>
          <div className="space-y-2">
            {dna.objections.map((o, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-md border border-white/[0.04] bg-white/[0.02] p-3"
              >
                <div>
                  <p className="text-[12px] font-medium">{o.topic}</p>
                  <p className="text-[11px] text-muted-foreground">
                    Raised {o.frequency}x · Last: {o.lastRaised}
                  </p>
                </div>
                <StatusBadge status={o.severity} />
              </div>
            ))}
          </div>
        </div>

        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Buying Signals
          </p>
          <div className="space-y-2">
            {dna.buyingSignals.map((s, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-md border border-white/[0.04] bg-white/[0.02] p-3"
              >
                <div>
                  <p className="text-[12px] font-medium">{s.signal}</p>
                  <p className="text-[11px] text-muted-foreground">{s.date}</p>
                </div>
                <StatusBadge
                  status={s.strength === "strong" ? "verified" : "pending"}
                />
              </div>
            ))}
          </div>
        </div>

        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Feature Request Frequency
          </p>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={dna.featureRequests} layout="vertical">
              <XAxis type="number" tick={{ fill: "#71717a", fontSize: 10 }} />
              <YAxis
                dataKey="feature"
                type="category"
                width={140}
                tick={{ fill: "#71717a", fontSize: 10 }}
              />
              <Tooltip
                contentStyle={{
                  background: "#18181b",
                  border: "1px solid rgba(255,255,255,0.08)",
                  fontSize: 11,
                }}
              />
              <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
