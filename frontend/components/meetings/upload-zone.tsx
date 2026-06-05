"use client";

import { useCallback, useState } from "react";
import { FileAudio, FileText, Upload } from "lucide-react";
import { cn } from "@/lib/utils";

interface UploadZoneProps {
  accept: "audio" | "transcript";
  onFileSelect: (file: File) => void;
}

export function UploadZone({ accept, onFileSelect }: UploadZoneProps) {
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) onFileSelect(file);
    },
    [onFileSelect]
  );

  const extensions =
    accept === "audio" ? ".mp3,.wav,.m4a,.webm" : ".txt,.md,.doc,.docx";

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-12 transition-colors",
        dragOver
          ? "border-primary bg-primary/5"
          : "border-border hover:border-primary/50 hover:bg-muted/30"
      )}
    >
      {accept === "audio" ? (
        <FileAudio className="h-12 w-12 text-muted-foreground" />
      ) : (
        <FileText className="h-12 w-12 text-muted-foreground" />
      )}
      <p className="mt-4 text-sm font-medium">
        Drag & drop your {accept === "audio" ? "audio file" : "transcript"}
      </p>
      <p className="mt-1 text-xs text-muted-foreground">
        or click to browse
      </p>
      <label className="mt-4 cursor-pointer">
        <span className="inline-flex items-center gap-2 rounded-lg bg-gradient-brand px-4 py-2 text-sm font-medium text-white hover:opacity-90">
          <Upload className="h-4 w-4" />
          Choose File
        </span>
        <input
          type="file"
          accept={extensions}
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) onFileSelect(file);
          }}
        />
      </label>
    </div>
  );
}
