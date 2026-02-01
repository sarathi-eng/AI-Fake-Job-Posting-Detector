"use client";

import { useState } from "react";
import { IconChevronDown, IconShieldCheck, IconShieldX } from "@tabler/icons-react";
import { cn } from "../lib/utils";
import SpotlightCard from "./SpotlightCard";

type Reason = {
  message: string;
};

type Sample = {
  label: "Legitimate" | "Fake";
  confidence: number;
  riskScore: number;
  reasons: Reason[];
};

const samples: Sample[] = [
  {
    label: "Legitimate",
    confidence: 88.5,
    riskScore: 15,
    reasons: [
      { message: "✓ No suspicious keywords detected" },
      { message: "✓ Company appears verifiable" },
      { message: "✓ Salary range appears realistic" },
    ],
  },
  {
    label: "Fake",
    confidence: 92.5,
    riskScore: 85,
    reasons: [
      { message: "⚠ Mentions payment / registration fee" },
      { message: "⚠ Excessive urgency / guaranteed job language" },
      { message: "⚠ Company details not verifiable" },
    ],
  },
];

export default function ExampleOutput() {
  return (
    <div>
      <h2 className="text-xl font-semibold">Example Output</h2>
      <p className="mt-2 max-w-3xl text-sm leading-6 text-white/75">
        Sample responses (formatted for readability). Your API returns structured
        JSON with classification, confidence, risk score, and reasons.
      </p>

      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {samples.map((s) => (
          <ExpandableResultCard key={s.label} sample={s} />
        ))}
      </div>

      <p className="mt-6 text-xs text-white/55">
        These are illustrative examples—do not treat them as benchmark results.
      </p>
    </div>
  );
}

function ExpandableResultCard({ sample }: { sample: Sample }) {
  const [open, setOpen] = useState(false);
  const isLegit = sample.label === "Legitimate";

  return (
    <SpotlightCard
      className={cn(
        "p-6",
        isLegit ? "border-emerald-500/15" : "border-rose-500/15"
      )}
      spotlightColor={isLegit ? "rgba(16, 185, 129, 0.22)" : "rgba(244, 63, 94, 0.22)"}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <div
            className={cn(
              "rounded-xl border p-2",
              isLegit
                ? "border-emerald-500/30 bg-emerald-500/10"
                : "border-rose-500/30 bg-rose-500/10"
            )}
          >
            {isLegit ? (
              <IconShieldCheck className="h-5 w-5 text-emerald-200" />
            ) : (
              <IconShieldX className="h-5 w-5 text-rose-200" />
            )}
          </div>
          <div>
            <div className="text-sm font-semibold">
              {isLegit ? "✅ Legit" : "❌ Fake"}
            </div>
            <div className="mt-2 text-sm text-white/70">
              <span className="text-white/85">Confidence:</span> {sample.confidence}%
              <span className="mx-2 text-white/30">•</span>
              <span className="text-white/85">Risk:</span> {sample.riskScore}/100
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className={cn(
            "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm",
            "hover:bg-white/10"
          )}
          aria-expanded={open}
        >
          <span className="inline-flex items-center gap-2">
            Reasons
            <IconChevronDown
              className={cn("h-4 w-4 transition-transform", open && "rotate-180")}
            />
          </span>
        </button>
      </div>

      {open && (
        <ul className="mt-5 space-y-2 text-sm text-white/75">
          {sample.reasons.map((r, idx) => (
            <li
              key={idx}
              className="rounded-xl border border-white/10 bg-bg-900/40 px-3 py-2"
            >
              {r.message}
            </li>
          ))}
        </ul>
      )}
    </SpotlightCard>
  );
}
