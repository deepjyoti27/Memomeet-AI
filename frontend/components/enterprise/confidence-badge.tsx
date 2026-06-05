import { cn } from "@/lib/utils";

export function ConfidenceBadge({
  score,
  size = "md",
}: {
  score: number;
  size?: "sm" | "md" | "lg";
}) {
  const color =
    score >= 90
      ? "text-emerald-400 border-emerald-500/30 bg-emerald-500/10"
      : score >= 70
        ? "text-amber-400 border-amber-500/30 bg-amber-500/10"
        : "text-red-400 border-red-500/30 bg-red-500/10";

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border font-mono font-semibold",
        color,
        size === "sm" && "px-1.5 py-0.5 text-[10px]",
        size === "md" && "px-2 py-0.5 text-xs",
        size === "lg" && "px-3 py-1 text-sm"
      )}
    >
      {score}%
    </span>
  );
}
