"use client";

import { useMemo, useState } from "react";

import { predictJob } from "../lib/api/client";
import { cn } from "../lib/utils";

type FormState = {
  title: string;
  company_name: string;
  description: string;
  salary_min: string;
  salary_max: string;
};

export default function TryItForm() {
  const apiBaseUrl = useMemo(() => {
    return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  }, []);

  const [form, setForm] = useState<FormState>({
    title: "Data Analyst",
    company_name: "Unknown Company",
    description:
      "Urgent hiring! No interview. Pay a small registration fee. WhatsApp us now.",
    salary_min: "",
    salary_max: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<
    | {
        classification: string;
        risk_score: number;
        confidence: number;
        reasons: { message: string }[];
      }
    | null
  >(null);

  const disabled = useMemo(() => {
    return (
      loading ||
      form.title.trim().length === 0 ||
      form.company_name.trim().length === 0 ||
      form.description.trim().length === 0
    );
  }, [form, loading]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);

    const salaryMin = form.salary_min.trim();
    const salaryMax = form.salary_max.trim();

    const payload = {
      title: form.title.trim(),
      company_name: form.company_name.trim(),
      description: form.description.trim(),
      currency: "INR",
      ...(salaryMin ? { salary_min: Number(salaryMin) } : {}),
      ...(salaryMax ? { salary_max: Number(salaryMax) } : {}),
    };

    try {
      setLoading(true);
      const res = await predictJob(payload);
      setResult(res);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Request failed";
      if (message.toLowerCase().includes("failed to fetch")) {
        setError(
          `Can't reach the API at ${apiBaseUrl}. ` +
            "Make sure the API is running and CORS allows this site origin (common when you open the web app via your LAN IP instead of localhost)."
        );
      } else {
        setError(message);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-sm font-semibold">Try it</div>
          <p className="mt-1 text-xs text-white/60">
            Paste a job post and get classification + risk score.
          </p>
        </div>
        <a
          href={apiBaseUrl + "/docs"}
          target="_blank"
          rel="noreferrer"
          className="text-xs text-white/70 underline decoration-white/20 underline-offset-4 hover:text-white"
        >
          Open Swagger
        </a>
      </div>

      <form onSubmit={onSubmit} className="mt-5 grid gap-3">
        <div className="grid gap-3 md:grid-cols-2">
          <Field
            label="Title"
            value={form.title}
            onChange={(v) => setForm((s) => ({ ...s, title: v }))}
          />
          <Field
            label="Company"
            value={form.company_name}
            onChange={(v) => setForm((s) => ({ ...s, company_name: v }))}
          />
        </div>

        <div>
          <div className="text-xs text-white/70">Description</div>
          <textarea
            value={form.description}
            onChange={(e) => setForm((s) => ({ ...s, description: e.target.value }))}
            rows={5}
            className={cn(
              "mt-2 w-full resize-y rounded-xl border border-white/10",
              "bg-bg-950/40 px-3 py-2 text-sm text-white/85",
              "placeholder:text-white/35",
              "focus:outline-none focus:ring-2 focus:ring-indigo-400/50"
            )}
            placeholder="Paste the job post text here…"
          />
        </div>

        <div className="grid gap-3 md:grid-cols-2">
          <Field
            label="Salary min (optional)"
            inputMode="numeric"
            value={form.salary_min}
            onChange={(v) => setForm((s) => ({ ...s, salary_min: v }))}
          />
          <Field
            label="Salary max (optional)"
            inputMode="numeric"
            value={form.salary_max}
            onChange={(v) => setForm((s) => ({ ...s, salary_max: v }))}
          />
        </div>

        <button
          type="submit"
          disabled={disabled}
          className={cn(
            "mt-1 inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium",
            "border border-indigo-500/45 bg-indigo-500/15 text-white",
            "hover:bg-indigo-500/20",
            "disabled:cursor-not-allowed disabled:opacity-60"
          )}
        >
          {loading ? "Analyzing…" : "Analyze"}
        </button>
      </form>

      {error && (
        <div className="mt-4 rounded-xl border border-rose-500/25 bg-rose-500/10 px-3 py-2 text-xs text-rose-100">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 rounded-2xl border border-white/10 bg-bg-900/40 p-4">
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="font-semibold">{result.classification}</span>
            <span className="text-white/40">•</span>
            <span className="text-white/75">Risk: {result.risk_score}/100</span>
            <span className="text-white/40">•</span>
            <span className="text-white/75">Confidence: {result.confidence}%</span>
          </div>

          <ul className="mt-3 space-y-2 text-xs text-white/70">
            {result.reasons.slice(0, 5).map((r, idx) => (
              <li key={idx} className="rounded-xl border border-white/10 bg-bg-950/40 px-3 py-2">
                {r.message}
              </li>
            ))}
          </ul>

          {result.reasons.length > 5 && (
            <div className="mt-2 text-[11px] text-white/50">
              Showing 5 of {result.reasons.length} reasons.
            </div>
          )}
        </div>
      )}

      <p className="mt-3 text-[11px] text-white/45">
        Tip: if the request fails, start the API and ensure CORS allows this site.
      </p>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  inputMode,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  inputMode?: React.HTMLAttributes<HTMLInputElement>["inputMode"];
}) {
  return (
    <label className="block">
      <div className="text-xs text-white/70">{label}</div>
      <input
        value={value}
        inputMode={inputMode}
        onChange={(e) => onChange(e.target.value)}
        className={cn(
          "mt-2 w-full rounded-xl border border-white/10",
          "bg-bg-950/40 px-3 py-2 text-sm text-white/85",
          "placeholder:text-white/35",
          "focus:outline-none focus:ring-2 focus:ring-indigo-400/50"
        )}
      />
    </label>
  );
}
