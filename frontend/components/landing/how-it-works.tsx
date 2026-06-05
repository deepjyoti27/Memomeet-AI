const steps = [
  {
    step: "01",
    title: "Record or Upload",
    description:
      "Upload meeting audio, paste a transcript, or record live from your browser.",
  },
  {
    step: "02",
    title: "AI Processes & Extracts",
    description:
      "Groq AI transcribes, identifies speakers, and extracts requirements, commitments, and deadlines.",
  },
  {
    step: "03",
    title: "Memory Stores Everything",
    description:
      "Hindsight Memory retains every insight with semantic search across all customer meetings.",
  },
  {
    step: "04",
    title: "Verify & Act",
    description:
      "Truth-verify claims, compare meetings, generate follow-ups, and track Meeting IQ scores.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="bg-muted/30 py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            How MemoMeet AI Works
          </h2>
          <p className="mt-4 text-muted-foreground">
            From raw meeting audio to actionable business intelligence in minutes.
          </p>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {steps.map(({ step, title, description }, i) => (
            <div key={step} className="relative">
              {i < steps.length - 1 && (
                <div className="absolute left-1/2 top-8 hidden h-0.5 w-full bg-gradient-brand lg:block" />
              )}
              <div className="relative flex flex-col items-center text-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-brand text-xl font-bold text-white shadow-lg">
                  {step}
                </div>
                <h3 className="mt-4 text-lg font-semibold">{title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">
                  {description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
