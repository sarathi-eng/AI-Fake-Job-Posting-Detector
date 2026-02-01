import {
  IconBuildingSkyscraper,
  IconCurrencyRupee,
  IconListSearch,
  IconSparkles,
} from "@tabler/icons-react";

import SpotlightCard from "./SpotlightCard";

const features = [
  {
    title: "Text Analysis",
    description:
      "Flags common scam language patterns, urgency tactics, and suspicious phrasing.",
    details: "Outputs text signals with confidence.",
    Icon: IconListSearch,
  },
  {
    title: "Company Verification",
    description:
      "Checks whether the company looks legitimate using verification heuristics and references.",
    details: "Highlights unverifiable or newly created entities.",
    Icon: IconBuildingSkyscraper,
  },
  {
    title: "Salary Anomaly Detection",
    description:
      "Detects unrealistic salary ranges or incomplete/too-good-to-be-true offers.",
    details: "Flags outliers vs. expected market patterns.",
    Icon: IconCurrencyRupee,
  },
  {
    title: "Explainable AI",
    description:
      "Returns clear reasons for why a post is risky—so humans can review quickly.",
    details: "Bulleted reasons + confidence per signal.",
    Icon: IconSparkles,
  },
] as const;

export default function Features() {
  return (
    <div>
      <h2 className="text-xl font-semibold">Features</h2>
      <p className="mt-2 max-w-2xl text-sm leading-6 text-white/75">
        Fast classification with clear, reviewable signals.
      </p>

      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {features.map((f) => (
          <SpotlightCard key={f.title} className="p-6">
            <div className="flex items-start gap-4">
              <div className="rounded-xl border border-white/10 bg-white/5 p-2">
                <f.Icon className="h-5 w-5 text-indigo-200" />
              </div>
              <div>
                <div className="text-sm font-semibold">{f.title}</div>
                <p className="mt-2 text-sm leading-6 text-white/75">
                  {f.description}
                </p>
                <p className="mt-3 text-xs text-white/60">{f.details}</p>
              </div>
            </div>
          </SpotlightCard>
        ))}
      </div>
    </div>
  );
}
