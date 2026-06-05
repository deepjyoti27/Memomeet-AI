import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: { value: number; positive: boolean };
  variant?: "default" | "gradient" | "warning" | "danger";
}

export function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  variant = "default",
}: StatCardProps) {
  return (
    <Card
      className={cn(
        "overflow-hidden transition-shadow hover:shadow-md",
        variant === "gradient" && "border-primary/20 bg-gradient-brand-subtle"
      )}
    >
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p
              className={cn(
                "text-3xl font-bold tracking-tight",
                variant === "gradient" && "gradient-text"
              )}
            >
              {value}
            </p>
            {subtitle && (
              <p className="text-xs text-muted-foreground">{subtitle}</p>
            )}
            {trend && (
              <p
                className={cn(
                  "text-xs font-medium",
                  trend.positive ? "text-emerald-600" : "text-red-500"
                )}
              >
                {trend.positive ? "+" : ""}
                {trend.value}% from last month
              </p>
            )}
          </div>
          <div
            className={cn(
              "rounded-lg p-3",
              variant === "warning" && "bg-amber-500/10 text-amber-600",
              variant === "danger" && "bg-red-500/10 text-red-500",
              variant === "gradient" && "bg-gradient-brand text-white",
              variant === "default" && "bg-primary/10 text-primary"
            )}
          >
            <Icon className="h-5 w-5" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
