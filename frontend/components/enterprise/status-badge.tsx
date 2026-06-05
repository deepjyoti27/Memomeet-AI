import { cn } from "@/lib/utils";

const styles: Record<string, string> = {
  active: "text-blue-400 border-blue-500/30 bg-blue-500/10",
  verified: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
  pending: "text-amber-400 border-amber-500/30 bg-amber-500/10",
  overdue: "text-red-400 border-red-500/30 bg-red-500/10",
  "at-risk": "text-orange-400 border-orange-500/30 bg-orange-500/10",
  unresolved: "text-red-400 border-red-500/30 bg-red-500/10",
  superseded: "text-muted-foreground border-white/10 bg-white/5",
  critical: "text-red-400 border-red-500/30 bg-red-500/10",
  high: "text-orange-400 border-orange-500/30 bg-orange-500/10",
  medium: "text-amber-400 border-amber-500/30 bg-amber-500/10",
  low: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
  elevated: "text-amber-400 border-amber-500/30 bg-amber-500/10",
};

export function StatusBadge({ status }: { status: string }) {
  return (
    <span
      className={cn(
        "inline-flex rounded-md border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider",
        styles[status] || styles.pending
      )}
    >
      {status.replace("-", " ")}
    </span>
  );
}
