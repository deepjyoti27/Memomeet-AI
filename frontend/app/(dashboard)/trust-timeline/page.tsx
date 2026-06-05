"use client";

import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  GitBranch,
  Minus,
  Plus,
} from "lucide-react";
import { PageHeader } from "@/components/enterprise/page-header";
import { StatusBadge } from "@/components/enterprise/status-badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { customers, trustTimeline } from "@/lib/enterprise-data";
import { cn } from "@/lib/utils";

const typeConfig: Record<
  string,
  { icon: typeof Plus; color: string; label: string }
> = {
  requirement_added: { icon: Plus, color: "text-blue-400", label: "Req Added" },
  requirement_removed: { icon: Minus, color: "text-red-400", label: "Req Removed" },
  decision: { icon: GitBranch, color: "text-violet-400", label: "Decision" },
  approval: { icon: CheckCircle2, color: "text-emerald-400", label: "Approval" },
  commitment: { icon: Clock, color: "text-amber-400", label: "Commitment" },
  objection: { icon: AlertTriangle, color: "text-orange-400", label: "Objection" },
  deadline: { icon: Clock, color: "text-red-400", label: "Deadline" },
  risk: { icon: AlertTriangle, color: "text-red-400", label: "Risk" },
};

export default function TrustTimelinePage() {
  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Trust Timeline™"
        title="Trust Timeline"
        description="Immutable audit trail of requirements, decisions, approvals, and risks across every interaction."
      >
        <Select defaultValue="all">
          <SelectTrigger className="w-48 border-white/[0.06] bg-white/[0.03]">
            <SelectValue placeholder="Filter account" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Accounts</SelectItem>
            {customers.map((c) => (
              <SelectItem key={c.id} value={c.id}>
                {c.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </PageHeader>

      <div className="relative">
        <div className="absolute left-[19px] top-0 h-full w-px bg-white/[0.08]" />

        <div className="space-y-1">
          {trustTimeline.map((event) => {
            const config = typeConfig[event.type] || typeConfig.decision;
            const Icon = config.icon;

            return (
              <div
                key={event.id}
                className="group relative flex gap-4 rounded-md py-3 pl-0 pr-4 transition-colors hover:bg-white/[0.02]"
              >
                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/[0.08] bg-[#111113]">
                  <Icon className={cn("h-4 w-4", config.color)} />
                </div>
                <div className="flex flex-1 items-start justify-between gap-4 border-b border-white/[0.04] pb-3 group-last:border-0">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                        {config.label}
                      </span>
                      <span className="font-mono text-[10px] text-muted-foreground">
                        {event.date}
                      </span>
                    </div>
                    <p className="mt-1 text-[13px] font-medium">{event.title}</p>
                    <p className="text-[11px] text-muted-foreground">
                      {event.customer}
                    </p>
                  </div>
                  <StatusBadge status={event.impact} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
