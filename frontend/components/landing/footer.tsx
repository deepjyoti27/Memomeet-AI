import { Sparkles } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-brand">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            <span className="font-semibold">MemoMeet AI</span>
          </div>
          <p className="text-sm text-muted-foreground">
            © 2026 MemoMeet AI. Meeting Intelligence & Memory Agent.
          </p>
        </div>
      </div>
    </footer>
  );
}
