import {
  AlertCircle,
  Calendar,
  CheckCircle2,
  GitBranch,
  MessageSquare,
  Users,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type EventType = "meeting" | "requirement" | "commitment" | "objection" | "decision";

interface TimelineEvent {
  id: string;
  date: string;
  type: EventType;
  title: string;
  description: string;
  customer: string;
}

const typeConfig: Record<
  EventType,
  { icon: typeof Calendar; color: string; label: string }
> = {
  meeting: { icon: MessageSquare, color: "bg-blue-500", label: "Meeting" },
  requirement: { icon: GitBranch, color: "bg-purple-500", label: "Requirement" },
  commitment: { icon: CheckCircle2, color: "bg-emerald-500", label: "Commitment" },
  objection: { icon: AlertCircle, color: "bg-amber-500", label: "Objection" },
  decision: { icon: Users, color: "bg-indigo-500", label: "Decision" },
};

export function TimelineView({ events }: { events: TimelineEvent[] }) {
  return (
    <div className="relative">
      <div className="absolute left-6 top-0 h-full w-0.5 bg-border md:left-1/2 md:-translate-x-px" />

      <div className="space-y-8">
        {events.map((event, i) => {
          const config = typeConfig[event.type];
          const Icon = config.icon;
          const isLeft = i % 2 === 0;

          return (
            <div
              key={event.id}
              className={cn(
                "relative flex items-start gap-4 md:gap-0",
                isLeft ? "md:flex-row" : "md:flex-row-reverse"
              )}
            >
              <div className="hidden w-1/2 md:block" />

              <div className="absolute left-6 z-10 flex h-12 w-12 -translate-x-1/2 items-center justify-center rounded-full border-4 border-background bg-card shadow-md md:left-1/2">
                <div
                  className={cn(
                    "flex h-8 w-8 items-center justify-center rounded-full text-white",
                    config.color
                  )}
                >
                  <Icon className="h-4 w-4" />
                </div>
              </div>

              <Card
                className={cn(
                  "ml-16 w-full md:ml-0 md:w-[calc(50%-2rem)]",
                  isLeft ? "md:mr-auto md:pr-8" : "md:ml-auto md:pl-8"
                )}
              >
                <CardContent className="p-4">
                  <div className="flex items-center justify-between gap-2">
                    <Badge variant="outline" className="text-[10px]">
                      {config.label}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {event.date}
                    </span>
                  </div>
                  <h3 className="mt-2 font-semibold">{event.title}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {event.description}
                  </p>
                </CardContent>
              </Card>
            </div>
          );
        })}
      </div>
    </div>
  );
}
