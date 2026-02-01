import TypewriterText from "./TypewriterText";
import ShinyButton from "./ShinyButton";

export default function Hero() {
  return (
    <div className="relative">
      <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-white/70">
        Production-ready API • Explainable risk scoring
      </div>

      <h1 className="mt-6 text-balance text-4xl font-semibold tracking-tight sm:text-5xl">
        Detect fake job posts{" "}
        <span className="bg-gradient-to-r from-indigo-200 via-white to-fuchsia-200 bg-clip-text text-transparent">
          <TypewriterText text="with AI." />
        </span>
      </h1>

      <p className="mt-5 max-w-2xl text-pretty text-sm leading-6 text-white/75">
        Simple REST API that returns classification, risk score, and reasons.
      </p>

      <div className="mt-8 flex flex-wrap gap-3">
        <ShinyButton href="#demo" variant="primary">
          Swagger docs
        </ShinyButton>
        <ShinyButton href="#features" variant="secondary">
          Features
        </ShinyButton>
      </div>

      <div className="mt-10 grid gap-3 sm:grid-cols-3">
        <Stat label="Signals" value="Text + Company + Salary" />
        <Stat label="Output" value="Legitimate / Suspicious / Fake" />
        <Stat label="Explainability" value="Reasons + confidence" />
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-4 shadow-glow">
      <div className="text-xs text-white/60">{label}</div>
      <div className="mt-1 text-sm font-medium">{value}</div>
    </div>
  );
}
