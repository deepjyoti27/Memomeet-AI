"use client";

import { useState } from "react";
import { BookOpen, Filter } from "lucide-react";
import { PageHeader } from "@/components/enterprise/page-header";
import { ConfidenceBadge } from "@/components/enterprise/confidence-badge";
import { StatusBadge } from "@/components/enterprise/status-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { commitments } from "@/lib/enterprise-data";

const types = ["All", "Requirement", "Commitment", "Approval", "Objection", "Deadline"];

export default function CommitmentLedgerPage() {
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");

  const filtered = commitments.filter((c) => {
    const matchType = filter === "All" || c.type === filter;
    const matchSearch =
      !search ||
      c.statement.toLowerCase().includes(search.toLowerCase()) ||
      c.customer.toLowerCase().includes(search.toLowerCase());
    return matchType && matchSearch;
  });

  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Commitment Ledger™"
        title="Commitment Ledger"
        description="Immutable record of every promise, requirement, deadline, objection, and approval — with confidence scores."
      />

      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap gap-1.5">
          {types.map((t) => (
            <Button
              key={t}
              variant="ghost"
              size="sm"
              onClick={() => setFilter(t)}
              className={`h-7 text-[11px] ${
                filter === t
                  ? "bg-white/[0.08] text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              {t}
            </Button>
          ))}
        </div>
        <div className="relative">
          <Input
            placeholder="Search ledger..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="h-8 w-64 border-white/[0.06] bg-white/[0.03] pl-8 text-[12px]"
          />
          <Filter className="absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
        </div>
      </div>

      <div className="overflow-hidden rounded-lg border border-white/[0.06]">
        <table className="w-full text-left text-[12px]">
          <thead>
            <tr className="border-b border-white/[0.06] bg-white/[0.02]">
              <th className="px-4 py-3 font-medium text-muted-foreground">Type</th>
              <th className="px-4 py-3 font-medium text-muted-foreground">Statement</th>
              <th className="px-4 py-3 font-medium text-muted-foreground">Owner</th>
              <th className="px-4 py-3 font-medium text-muted-foreground">Speaker</th>
              <th className="px-4 py-3 font-medium text-muted-foreground">Meeting</th>
              <th className="px-4 py-3 font-medium text-muted-foreground">Status</th>
              <th className="px-4 py-3 font-medium text-muted-foreground">Conf.</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((c) => (
              <tr
                key={c.id}
                className="border-b border-white/[0.04] transition-colors hover:bg-white/[0.02]"
              >
                <td className="px-4 py-3">
                  <span className="flex items-center gap-1.5">
                    <BookOpen className="h-3 w-3 text-muted-foreground" />
                    {c.type}
                  </span>
                </td>
                <td className="max-w-xs px-4 py-3">
                  <p className="line-clamp-2">{c.statement}</p>
                  <p className="mt-0.5 text-[10px] text-muted-foreground">
                    {c.customer}
                  </p>
                </td>
                <td className="px-4 py-3 text-muted-foreground">{c.owner}</td>
                <td className="px-4 py-3">{c.speaker}</td>
                <td className="px-4 py-3">
                  <p>{c.meetingTitle}</p>
                  <p className="font-mono text-[10px] text-muted-foreground">
                    {c.meetingDate}
                  </p>
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={c.status} />
                </td>
                <td className="px-4 py-3">
                  <ConfidenceBadge score={c.confidence} size="sm" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-3 font-mono text-[11px] text-muted-foreground">
        Showing {filtered.length} of {commitments.length} ledger entries
      </p>
    </div>
  );
}
