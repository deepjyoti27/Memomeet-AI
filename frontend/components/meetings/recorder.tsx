"use client";

import { useEffect, useRef, useState } from "react";
import { Mic, Square } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function MeetingRecorder() {
  const [recording, setRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (recording) {
      intervalRef.current = setInterval(() => {
        setDuration((d) => d + 1);
      }, 1000);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [recording]);

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
  };

  return (
    <div className="flex flex-col items-center rounded-xl border border-border p-12">
      <div
        className={cn(
          "relative flex h-24 w-24 items-center justify-center rounded-full",
          recording
            ? "bg-red-500/10 ring-4 ring-red-500/30"
            : "bg-muted"
        )}
      >
        {recording && (
          <span className="absolute inset-0 animate-ping rounded-full bg-red-500/20" />
        )}
        <Mic
          className={cn(
            "h-10 w-10",
            recording ? "text-red-500" : "text-muted-foreground"
          )}
        />
      </div>

      <p className="mt-6 font-mono text-3xl font-bold">{formatTime(duration)}</p>
      <p className="mt-2 text-sm text-muted-foreground">
        {recording ? "Recording in progress..." : "Ready to record"}
      </p>

      <Button
        variant={recording ? "destructive" : "gradient"}
        size="lg"
        className="mt-6 gap-2"
        onClick={() => {
          if (recording) {
            setRecording(false);
          } else {
            setDuration(0);
            setRecording(true);
          }
        }}
      >
        {recording ? (
          <>
            <Square className="h-4 w-4" />
            Stop Recording
          </>
        ) : (
          <>
            <Mic className="h-4 w-4" />
            Start Recording
          </>
        )}
      </Button>
    </div>
  );
}
