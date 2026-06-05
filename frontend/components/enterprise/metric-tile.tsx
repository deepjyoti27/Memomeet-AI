import { LucideIcon, TrendingDown, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface MetricTileProps {
  label: string;
  value: string | number;
  delta?: number;
  icon: LucideIcon;
  suffix?: string;
  variant?: "default" | "danger" | "success";
}

export function MetricTile({
  label,
  value,
  delta,
  icon: Icon,
  suffix,
  variant = "default",
}: MetricTileProps) {
  const positive = delta !== undefined && delta >= 0;

  return (
    <div
      className={cn(
        "intel-panel stat-glow group",
        variant === "danger" && "border-red-500/20",
        variant === "success" && "border-emerald-500/20"
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-3">
          <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            {label}
          </p>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-semibold tracking-tight">{value}</span>
            {suffix && (
              <span className="text-sm text-muted-foreground">{suffix}</span>
            )}
          </div>
          {delta !== undefined && (
            <div
              className={cn(
                "flex items-center gap-1 text-xs font-medium",
                positive ? "text-emerald-400" : "text-red-400"
              )}
            >
              {positive ? (
                <TrendingUp className="h-3 w-3" />
              ) : (
                <TrendingDown className="h-3 w-3" />
              )}
              {Math.abs(delta)}% vs last month
            </div>
          )}
        </div>
        <div className="rounded-md border border-white/[0.06] bg-white/[0.02] p-2.5 text-muted-foreground transition-colors group-hover:text-foreground">
          <Icon className="h-4 w-4" />
        </div>
      </div>
    </div>
  );
}
