"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Upload,
  Shield,
  Dna,
  GitBranch,
  GitCompare,
  BookOpen,
  Radar,
  Hexagon,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/upload", label: "Upload Meeting", icon: Upload },
  { href: "/truth-engine", label: "Truth Engine", icon: Shield },
  { href: "/customer-dna", label: "Customer DNA", icon: Dna },
  { href: "/trust-timeline", label: "Trust Timeline", icon: GitBranch },
  { href: "/meeting-comparison", label: "Meeting Comparison", icon: GitCompare },
  { href: "/commitment-ledger", label: "Commitment Ledger", icon: BookOpen },
  { href: "/risk-radar", label: "Risk Radar", icon: Radar },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-[240px] shrink-0 flex-col border-r border-white/[0.06] bg-[#0a0a0b] lg:flex">
      <div className="flex h-14 items-center gap-2.5 border-b border-white/[0.06] px-5">
        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-gradient-to-br from-blue-500 to-violet-600">
          <Hexagon className="h-3.5 w-3.5 text-white" />
        </div>
        <div>
          <p className="text-[13px] font-semibold tracking-tight">MemoMeet</p>
          <p className="text-[9px] uppercase tracking-widest text-muted-foreground">
            Truth Intelligence
          </p>
        </div>
      </div>

      <nav className="flex-1 space-y-0.5 p-3">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active =
            pathname === href || pathname.startsWith(href + "/");
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-2.5 rounded-md px-3 py-2 text-[13px] font-medium transition-all",
                active
                  ? "bg-white/[0.08] text-foreground"
                  : "text-muted-foreground hover:bg-white/[0.04] hover:text-foreground"
              )}
            >
              <Icon
                className={cn(
                  "h-4 w-4",
                  active ? "text-blue-400" : "text-muted-foreground"
                )}
              />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-white/[0.06] p-3">
        <div className="rounded-md border border-white/[0.06] bg-white/[0.02] p-3">
          <div className="flex items-center justify-between">
            <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
              Memory Index
            </p>
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
          </div>
          <p className="mt-1 font-mono text-lg font-semibold">1,847</p>
          <p className="text-[10px] text-muted-foreground">
            commitments across 34 accounts
          </p>
        </div>
      </div>
    </aside>
  );
}
