"use client";

import Link from "next/link";
import {
  AlertTriangle,
  BookOpen,
  Brain,
  Radar,
  Shield,
  TrendingUp,
} from "lucide-react";
import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { PageHeader } from "@/components/enterprise/page-header";
import { CustomerCommitmentScore } from "@/components/enterprise/customer-commitment-score";
import { MetricTile } from "@/components/enterprise/metric-tile";
import { StatusBadge } from "@/components/enterprise/status-badge";
import { Button } from "@/components/ui/button";
import {
  dashboardMetrics,
  activityFeed,
  riskRadar,
  meetingIQ,
  customerDNA,
} from "@/lib/enterprise-data";

export default function DashboardPage() {
  return (
    <div className="animate-fade-up">
      <PageHeader
        badge="Command Center"
        title="Intelligence Dashboard"
        description="Real-time view of commitments, truth queries, drift alerts, and account risk across your portfolio."
      >
        <Button
          size="sm"
          asChild
          className="bg-white text-black hover:bg-white/90"
        >
          <Link href="/upload">Upload Meeting</Link>
        </Button>
      </PageHeader>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricTile
          label="Commitments Tracked"
          value={dashboardMetrics.commitmentsTracked.toLocaleString()}
          delta={dashboardMetrics.commitmentsDelta}
          icon={BookOpen}
        />
        <MetricTile
          label="Truth Queries"
          value={dashboardMetrics.truthQueries}
          delta={dashboardMetrics.truthQueriesDelta}
          icon={Shield}
        />
        <MetricTile
          label="Drift Alerts"
          value={dashboardMetrics.driftAlerts}
          delta={dashboardMetrics.driftAlertsDelta}
          icon={TrendingUp}
          variant="danger"
        />
        <MetricTile
          label="At-Risk Accounts"
          value={dashboardMetrics.atRiskAccounts}
          icon={Radar}
          variant="danger"
        />
      </div>

      <div className="mt-4 grid gap-4 sm:grid-cols-3">
        <MetricTile
          label="Avg Meeting IQ"
          value={dashboardMetrics.avgMeetingIQ}
          suffix="/ 100"
          icon={Brain}
        />
        <MetricTile
          label="Disputes Resolved"
          value={`${dashboardMetrics.disputedClaimsResolved}%`}
          icon={Shield}
          variant="success"
        />
        <MetricTile
          label="Memory Retention"
          value={dashboardMetrics.memoryRetention}
          icon={BookOpen}
          variant="success"
        />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <CustomerCommitmentScore
          data={customerDNA.profile.commitmentScore}
          compact
        />

        {/* Sentiment chart */}
        <div className="intel-panel lg:col-span-2">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Portfolio Sentiment — Acme Corporation
          </p>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={customerDNA.profile.sentimentTrend}>
              <defs>
                <linearGradient id="sentGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.2} />
                  <stop offset="100%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="month"
                tick={{ fill: "#71717a", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fill: "#71717a", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  background: "#18181b",
                  border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Area
                type="monotone"
                dataKey="score"
                stroke="#3b82f6"
                fill="url(#sentGrad)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Activity feed */}
        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Live Activity
          </p>
          <div className="space-y-3">
            {activityFeed.map((item, i) => (
              <div
                key={i}
                className="flex gap-3 border-b border-white/[0.04] pb-3 last:border-0 last:pb-0"
              >
                <span className="shrink-0 font-mono text-[10px] text-muted-foreground">
                  {item.time}
                </span>
                <div>
                  <p className="text-[12px] font-medium">{item.event}</p>
                  <p className="text-[11px] text-muted-foreground">
                    {item.detail}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {/* Risk alerts */}
        <div className="intel-panel">
          <div className="mb-4 flex items-center justify-between">
            <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
              Critical Alerts
            </p>
            <Button variant="ghost" size="sm" asChild className="h-7 text-[11px]">
              <Link href="/risk-radar">View Radar →</Link>
            </Button>
          </div>
          <div className="space-y-2">
            {riskRadar.alerts.slice(0, 4).map((alert) => (
              <div
                key={alert.id}
                className="flex items-start justify-between rounded-md border border-white/[0.04] bg-white/[0.02] p-3"
              >
                <div className="flex gap-2">
                  <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-red-400" />
                  <div>
                    <p className="text-[12px] font-medium">{alert.title}</p>
                    <p className="text-[11px] text-muted-foreground">
                      {alert.customer} · {alert.daysOpen}d open
                    </p>
                  </div>
                </div>
                <StatusBadge status={alert.severity} />
              </div>
            ))}
          </div>
        </div>

        {/* Recent Meeting IQ */}
        <div className="intel-panel">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            Recent Meeting IQ™
          </p>
          <div className="space-y-2">
            {meetingIQ.recentMeetings.map((m, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-md border border-white/[0.04] bg-white/[0.02] p-3"
              >
                <div>
                  <p className="text-[12px] font-medium">{m.title}</p>
                  <p className="text-[11px] text-muted-foreground">
                    {m.customer} · {m.date}
                  </p>
                </div>
                <div className="text-right">
                  <p
                    className={`font-mono text-lg font-semibold ${m.iq >= 75 ? "text-emerald-400" : m.iq >= 60 ? "text-amber-400" : "text-red-400"}`}
                  >
                    {m.iq}
                  </p>
                  <p className="text-[10px] text-muted-foreground">IQ Score</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
