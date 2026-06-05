import { CheckCircle2, XCircle } from "lucide-react";

const problems = [
  "Important commitments forgotten after meetings",
  "Customers dispute what was agreed upon",
  "Requirements change without documentation",
  "No visibility into customer needs over time",
];

const solutions = [
  "AI memory retains every commitment and decision",
  "Truth Verification finds evidence in seconds",
  "Timeline tracks requirement evolution",
  "Intelligence dashboard reveals patterns and risks",
];

export function WhyMemoMeet() {
  return (
    <section id="why" className="py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Why MemoMeet AI?
          </h2>
          <p className="mt-4 text-muted-foreground">
            Built for the real problems enterprise teams face every day.
          </p>
        </div>

        <div className="mt-16 grid gap-8 lg:grid-cols-2">
          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-8">
            <h3 className="text-lg font-semibold text-red-600 dark:text-red-400">
              Without MemoMeet
            </h3>
            <ul className="mt-6 space-y-4">
              {problems.map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <XCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
                  <span className="text-sm text-muted-foreground">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-8">
            <h3 className="text-lg font-semibold text-emerald-600 dark:text-emerald-400">
              With MemoMeet AI
            </h3>
            <ul className="mt-6 space-y-4">
              {solutions.map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-500" />
                  <span className="text-sm text-muted-foreground">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
