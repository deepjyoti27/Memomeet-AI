"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Shield,
  BookOpen,
  Radar,
  Menu,
} from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const primaryNav = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Home" },
  { href: "/truth-engine", icon: Shield, label: "Truth" },
  { href: "/commitment-ledger", icon: BookOpen, label: "Ledger" },
  { href: "/risk-radar", icon: Radar, label: "Risk" },
];

const allNav = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/upload", label: "Upload Meeting" },
  { href: "/truth-engine", label: "Truth Engine" },
  { href: "/customer-dna", label: "Customer DNA" },
  { href: "/trust-timeline", label: "Trust Timeline" },
  { href: "/meeting-comparison", label: "Meeting Comparison" },
  { href: "/commitment-ledger", label: "Commitment Ledger" },
  { href: "/risk-radar", label: "Risk Radar" },
];

export function MobileNav() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <>
      <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-white/[0.06] bg-[#0a0a0b]/95 backdrop-blur-xl lg:hidden">
        <div className="flex items-center justify-around py-2">
          {primaryNav.map(({ href, icon: Icon, label }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex flex-col items-center gap-0.5 px-3 py-1",
                pathname === href ? "text-blue-400" : "text-muted-foreground"
              )}
            >
              <Icon className="h-5 w-5" />
              <span className="text-[10px]">{label}</span>
            </Link>
          ))}
          <button
            onClick={() => setOpen(true)}
            className="flex flex-col items-center gap-0.5 px-3 py-1 text-muted-foreground"
          >
            <Menu className="h-5 w-5" />
            <span className="text-[10px]">More</span>
          </button>
        </div>
      </nav>

      {open && (
        <div
          className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setOpen(false)}
        >
          <div
            className="absolute bottom-16 left-4 right-4 rounded-lg border border-white/[0.08] bg-[#111113] p-2"
            onClick={(e) => e.stopPropagation()}
          >
            {allNav.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                onClick={() => setOpen(false)}
                className={cn(
                  "block rounded-md px-4 py-2.5 text-sm",
                  pathname === href
                    ? "bg-white/[0.08] text-foreground"
                    : "text-muted-foreground"
                )}
              >
                {label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
