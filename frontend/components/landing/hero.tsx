import Link from "next/link";
import { ArrowRight, Brain, Shield, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-32 pb-20">
      <div className="absolute inset-0 bg-gradient-brand opacity-[0.03]" />
      <div className="absolute -top-40 right-0 h-96 w-96 rounded-full bg-brand-purple/20 blur-3xl" />
      <div className="absolute -bottom-40 left-0 h-96 w-96 rounded-full bg-brand-blue/20 blur-3xl" />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <Badge variant="secondary" className="mb-6 gap-1">
            <Sparkles className="h-3 w-3" />
            AI-Powered Meeting Intelligence
          </Badge>

          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
            Your Second Brain for{" "}
            <span className="gradient-text">Every Business Meeting</span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl">
            MemoMeet AI records, analyzes, remembers, and verifies every
            commitment, requirement, and decision — so nothing gets lost or
            disputed.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Button variant="gradient" size="lg" asChild>
              <Link href="/dashboard">
                Start Free Trial
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="#how-it-works">See How It Works</Link>
            </Button>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-4 sm:grid-cols-3">
            {[
              { icon: Brain, label: "AI Memory", desc: "Never forget a commitment" },
              { icon: Shield, label: "Truth Verify", desc: "Prove what was discussed" },
              { icon: Sparkles, label: "Meeting IQ", desc: "Score every meeting" },
            ].map(({ icon: Icon, label, desc }) => (
              <div
                key={label}
                className="glass-card flex flex-col items-center p-6"
              >
                <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-brand text-white">
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="font-semibold">{label}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
