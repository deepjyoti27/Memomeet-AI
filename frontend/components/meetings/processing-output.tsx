import {
  Calendar,
  CheckCircle2,
  ClipboardList,
  Gavel,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { processedMeetingOutput } from "@/lib/mock-data";

export function ProcessingOutput() {
  const { summary, actionItems, decisions, deadlines } = processedMeetingOutput;

  return (
    <div className="space-y-6">
      <Card className="border-primary/20 bg-gradient-brand-subtle">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="h-4 w-4 text-primary" />
            AI Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm leading-relaxed">{summary}</p>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base">
              <ClipboardList className="h-4 w-4" />
              Action Items
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {actionItems.map((item, i) => (
              <div
                key={i}
                className="flex items-start justify-between rounded-lg border border-border p-3"
              >
                <div>
                  <p className="text-sm font-medium">{item.task}</p>
                  <p className="text-xs text-muted-foreground">
                    Owner: {item.owner}
                  </p>
                </div>
                <Badge variant="outline">{item.due}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base">
              <Gavel className="h-4 w-4" />
              Key Decisions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {decisions.map((decision, i) => (
              <div key={i} className="flex items-start gap-2">
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
                <p className="text-sm">{decision}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-base">
            <Calendar className="h-4 w-4" />
            Deadlines
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-3">
            {deadlines.map((dl, i) => (
              <div
                key={i}
                className="rounded-lg border border-border p-4 text-center"
              >
                <p className="text-sm font-medium">{dl.item}</p>
                <p className="mt-1 text-lg font-bold">{dl.date}</p>
                <Badge
                  variant={
                    dl.status === "at-risk"
                      ? "danger"
                      : dl.status === "pending"
                        ? "warning"
                        : "success"
                  }
                  className="mt-2"
                >
                  {dl.status}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
