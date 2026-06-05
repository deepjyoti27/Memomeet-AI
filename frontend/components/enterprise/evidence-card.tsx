import { Calendar, Clock, FileText, User } from "lucide-react";
import { ConfidenceBadge } from "./confidence-badge";

interface EvidenceCardProps {
  statement: string;
  speaker: string;
  role?: string;
  meetingDate: string;
  meetingTitle: string;
  timestamp?: string;
  confidence: number;
  transcriptId?: string;
}

export function EvidenceCard({
  statement,
  speaker,
  role,
  meetingDate,
  meetingTitle,
  timestamp,
  confidence,
  transcriptId,
}: EvidenceCardProps) {
  return (
    <div className="enterprise-card-hover gradient-border-top overflow-hidden">
      <div className="border-b border-white/[0.04] bg-white/[0.02] px-5 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
              <User className="h-3.5 w-3.5" />
            </div>
            <div>
              <p className="text-sm font-medium">{speaker}</p>
              {role && (
                <p className="text-[11px] text-muted-foreground">{role}</p>
              )}
            </div>
          </div>
          <ConfidenceBadge score={confidence} />
        </div>
      </div>
      <div className="p-5">
        <blockquote className="border-l-2 border-blue-500/40 pl-4 text-sm leading-relaxed text-foreground/90">
          &ldquo;{statement}&rdquo;
        </blockquote>
        <div className="mt-4 flex flex-wrap items-center gap-4 text-[11px] text-muted-foreground">
          <span className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            {meetingDate}
          </span>
          <span>{meetingTitle}</span>
          {timestamp && (
            <span className="flex items-center gap-1 font-mono">
              <Clock className="h-3 w-3" />
              {timestamp}
            </span>
          )}
          {transcriptId && (
            <span className="flex items-center gap-1 font-mono">
              <FileText className="h-3 w-3" />
              {transcriptId}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
