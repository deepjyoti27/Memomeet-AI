"use client";

import { useState } from "react";
import { Loader2, Search, Shield } from "lucide-react";
import { PageHeader } from "@/components/enterprise/page-header";
import { EvidenceCard } from "@/components/enterprise/evidence-card";
import { ConfidenceBadge } from "@/components/enterprise/confidence-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { customers, truthEngineResult } from "@/lib/enterprise-data";

export default function TruthEnginePage() {
  const [query, setQuery] = useState(truthEngineResult.query);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<typeof truthEngineResult | null>(null);

  const search = () => {
    setLoading(true);
    setResult(null);
    setTimeout(() => {
      setLoading(false);
      setResult(truthEngineResult);
    }, 1800);
  };

  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Business Truth Engine™"
        title="Truth Engine"
        description="Query your entire meeting memory. Get exact statements, evidence scores, and transcript sources."
      />

      <div className="intel-panel mb-6">
        <div className="flex items-start gap-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
            <Shield className="h-5 w-5" />
          </div>
          <div className="flex-1 space-y-4">
            <div className="grid gap-4 sm:grid-cols-4">
              <div className="sm:col-span-1">
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
              <div className="sm:col-span-3">
                <label className="mb-1.5 block text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  Truth Query
                </label>
                <div className="flex gap-2">
                  <Input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder='e.g. "Did customer ever approve pricing?"'
                    className="border-white/[0.06] bg-white/[0.03] font-mono text-[13px]"
                  />
                  <Button
                    onClick={search}
                    disabled={loading}
                    className="shrink-0 bg-white text-black hover:bg-white/90"
                  >
                    {loading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Search className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {loading && (
        <div className="intel-panel flex flex-col items-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-blue-400" />
          <p className="mt-4 text-sm font-medium">
            Searching 1,847 indexed commitments...
          </p>
          <p className="mt-1 font-mono text-[11px] text-muted-foreground">
            Hindsight Memory · Semantic Recall · Transcript Match
          </p>
        </div>
      )}

      {result && (
        <div className="space-y-6">
          <div className="intel-panel border-amber-500/20">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-[11px] font-medium uppercase tracking-wider text-amber-400">
                  Verdict: Partially Verified
                </p>
                <p className="mt-2 max-w-2xl text-[13px] leading-relaxed text-muted-foreground">
                  {result.summary}
                </p>
              </div>
              <ConfidenceBadge score={result.confidence} size="lg" />
            </div>
          </div>

          <div>
            <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Evidence — {result.evidence.length} matches
            </p>
            <div className="space-y-3">
              {result.evidence.map((e, i) => (
                <EvidenceCard key={i} {...e} />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
