"use client";

import { useState } from "react";
import { FileAudio, FileText, Loader2, Upload } from "lucide-react";
import { PageHeader } from "@/components/enterprise/page-header";
import { ConfidenceBadge } from "@/components/enterprise/confidence-badge";
import { StatusBadge } from "@/components/enterprise/status-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { customers } from "@/lib/enterprise-data";

const extractedCommitments = [
  { type: "Requirement", statement: "Salesforce sandbox credentials within 5 business days", owner: "Customer", confidence: 93 },
  { type: "Commitment", statement: "Revised enterprise pricing proposal by June 8", owner: "Internal", confidence: 97 },
  { type: "Decision", statement: "Q3 campaign launch contingent on CRM go-live", owner: "Joint", confidence: 91 },
  { type: "Deadline", statement: "CRM integration live by September 30", owner: "Customer", confidence: 97 },
];

export default function UploadPage() {
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [complete, setComplete] = useState(false);

  const process = () => {
    setProcessing(true);
    setProgress(0);
    setComplete(false);
    const iv = setInterval(() => {
      setProgress((p) => {
        if (p >= 100) {
          clearInterval(iv);
          setProcessing(false);
          setComplete(true);
          return 100;
        }
        return p + 8;
      });
    }, 300);
  };

  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Ingestion"
        title="Upload Meeting"
        description="Extract commitments, requirements, and decisions into the Commitment Ledger™ automatically."
      />

      <div className="intel-panel mb-6">
        <div className="grid gap-4 sm:grid-cols-3">
          <div>
            <label className="mb-1.5 block text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Account
            </label>
            <Select defaultValue="acme">
              <SelectTrigger className="border-white/[0.06] bg-white/[0.03]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {customers.map((c) => (
                  <SelectItem key={c.id} value={c.id}>
                    {c.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="mb-1.5 block text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Meeting Title
            </label>
            <Input
              defaultValue="Q2 Planning Review"
              className="border-white/[0.06] bg-white/[0.03]"
            />
          </div>
          <div>
            <label className="mb-1.5 block text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Date
            </label>
            <Input
              type="date"
              defaultValue="2026-06-01"
              className="border-white/[0.06] bg-white/[0.03]"
            />
          </div>
        </div>
      </div>

      <Tabs defaultValue="audio">
        <TabsList className="border border-white/[0.06] bg-white/[0.03]">
          <TabsTrigger value="audio" className="text-[12px]">
            Audio Upload
          </TabsTrigger>
          <TabsTrigger value="transcript" className="text-[12px]">
            Transcript
          </TabsTrigger>
        </TabsList>

        <TabsContent value="audio" className="mt-4">
          <div
            onClick={process}
            className="enterprise-card-hover flex cursor-pointer flex-col items-center justify-center p-16"
          >
            <FileAudio className="h-10 w-10 text-muted-foreground" />
            <p className="mt-4 text-sm font-medium">
              Drop audio file or click to upload
            </p>
            <p className="mt-1 text-[11px] text-muted-foreground">
              MP3, WAV, M4A · Max 500MB
            </p>
            <Button size="sm" className="mt-4 gap-1.5 bg-white text-black hover:bg-white/90">
              <Upload className="h-3.5 w-3.5" />
              Select File
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="transcript" className="mt-4">
          <div
            onClick={process}
            className="enterprise-card-hover flex cursor-pointer flex-col items-center justify-center p-16"
          >
            <FileText className="h-10 w-10 text-muted-foreground" />
            <p className="mt-4 text-sm font-medium">
              Drop transcript or click to upload
            </p>
            <p className="mt-1 text-[11px] text-muted-foreground">
              TXT, DOCX, PDF
            </p>
          </div>
        </TabsContent>
      </Tabs>

      {processing && (
        <div className="intel-panel mt-6">
          <div className="flex items-center gap-3">
            <Loader2 className="h-4 w-4 animate-spin text-blue-400" />
            <div className="flex-1">
              <p className="text-[13px] font-medium">
                Extracting commitments into Ledger...
              </p>
              <p className="text-[11px] text-muted-foreground">
                Transcribe → Diarize → Extract → Index → Sync Memory
              </p>
              <Progress value={progress} className="mt-3 h-1" />
            </div>
            <span className="font-mono text-sm">{progress}%</span>
          </div>
        </div>
      )}

      {complete && (
        <div className="mt-6 space-y-4">
          <div className="intel-panel border-emerald-500/20">
            <p className="text-[11px] font-medium uppercase tracking-wider text-emerald-400">
              Extraction Complete — 4 commitments indexed
            </p>
            <p className="mt-2 text-[13px] text-muted-foreground">
              Meeting processed. Commitments added to Ledger. Drift detection
              and risk radar updated.
            </p>
          </div>

          <div className="overflow-hidden rounded-lg border border-white/[0.06]">
            <table className="w-full text-left text-[12px]">
              <thead>
                <tr className="border-b border-white/[0.06] bg-white/[0.02]">
                  <th className="px-4 py-3 font-medium text-muted-foreground">Type</th>
                  <th className="px-4 py-3 font-medium text-muted-foreground">Statement</th>
                  <th className="px-4 py-3 font-medium text-muted-foreground">Owner</th>
                  <th className="px-4 py-3 font-medium text-muted-foreground">Confidence</th>
                </tr>
              </thead>
              <tbody>
                {extractedCommitments.map((c, i) => (
                  <tr key={i} className="border-b border-white/[0.04] hover:bg-white/[0.02]">
                    <td className="px-4 py-3">
                      <StatusBadge status="active" />
                      <span className="ml-2">{c.type}</span>
                    </td>
                    <td className="px-4 py-3">{c.statement}</td>
                    <td className="px-4 py-3 text-muted-foreground">{c.owner}</td>
                    <td className="px-4 py-3">
                      <ConfidenceBadge score={c.confidence} size="sm" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
