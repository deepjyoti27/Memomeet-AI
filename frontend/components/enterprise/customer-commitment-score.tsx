"use client";

import { AlertTriangle, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

export interface CommitmentDimension {
  label: string;
  score: number;
  status: "strong" | "weak" | "hesitant" | "moderate";
  evidence?: string;
}

export interface CommitmentScoreData {
  overall: number;
  dimensions: CommitmentDimension[];
  warning?: {
    title: string;
    message: string;
    severity: "high" | "medium" | "low";
    source?: string;
  };
}

function scoreColor(score: number) {
  if (score >= 80) return { bar: "bg-emerald-500", text: "text-emerald-400" };
  if (score >= 60) return { bar: "bg-amber-500", text: "text-amber-400" };
  return { bar: "bg-red-500", text: "text-red-400" };
}

function ScoreBar({
  label,
  score,
  evidence,
}: {
  label: string;
  score: number;
  evidence?: string;
}) {
  const colors = scoreColor(score);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-[13px] font-medium">{label}</span>
        <span className={cn("font-mono text-sm font-semibold", colors.text)}>
          {score}%
        </span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-white/[0.06]">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-700",
            colors.bar
          )}
          style={{ width: `${score}%` }}
        />
      </div>
      {evidence && (
        <p className="text-[11px] leading-relaxed text-muted-foreground">
          {evidence}
        </p>
      )}
    </div>
  );
}

interface CustomerCommitmentScoreProps {
  data: CommitmentScoreData;
  customer?: string;
  compact?: boolean;
}

export function CustomerCommitmentScore({
  data,
  customer,
  compact = false,
}: CustomerCommitmentScoreProps) {
  const overallColors = scoreColor(data.overall);

  if (compact) {
    return (
      <div className="intel-panel">
        <div className="mb-4 flex items-center justify-between">
          <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Customer Commitment Score
          </p>
          <span
            className={cn(
              "font-mono text-lg font-semibold",
              overallColors.text
            )}
          >
            {data.overall}%
          </span>
        </div>
        <div className="space-y-3">
          {data.dimensions.map((d) => (
            <div key={d.label} className="flex items-center justify-between">
              <span className="text-[11px] text-muted-foreground">
                {d.label}
              </span>
              <span
                className={cn(
                  "font-mono text-[12px] font-semibold",
                  scoreColor(d.score).text
                )}
              >
                {d.score}%
              </span>
            </div>
          ))}
        </div>
        {data.warning && (
          <div className="mt-4 flex gap-2 rounded-md border border-amber-500/20 bg-amber-500/5 p-3">
            <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-400" />
            <p className="text-[11px] text-amber-200/80">{data.warning.message}</p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="intel-panel gradient-border-top">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-blue-400" />
            <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-400">
              Customer Commitment Score™
            </p>
          </div>
          {customer && (
            <p className="mt-1 text-[13px] text-muted-foreground">{customer}</p>
          )}
        </div>
        <div className="text-left sm:text-right">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
            Overall Alignment
          </p>
          <p
            className={cn(
              "font-mono text-4xl font-semibold tracking-tight",
              overallColors.text
            )}
          >
            {data.overall}%
          </p>
        </div>
      </div>

      <div className="space-y-5">
        {data.dimensions.map((d) => (
          <ScoreBar
            key={d.label}
            label={d.label}
            score={d.score}
            evidence={d.evidence}
          />
        ))}
      </div>

      {data.warning && (
        <div
          className={cn(
            "mt-6 flex gap-3 rounded-lg border p-4",
            data.warning.severity === "high"
              ? "border-amber-500/25 bg-amber-500/5"
              : "border-white/[0.06] bg-white/[0.02]"
          )}
        >
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-amber-500/10">
            <AlertTriangle className="h-4 w-4 text-amber-400" />
          </div>
          <div>
            <p className="text-[12px] font-semibold text-amber-400">
              Warning: {data.warning.title}
            </p>
            <p className="mt-1 text-[12px] leading-relaxed text-muted-foreground">
              {data.warning.message}
            </p>
            {data.warning.source && (
              <p className="mt-2 font-mono text-[10px] text-muted-foreground/70">
                Source: {data.warning.source}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
