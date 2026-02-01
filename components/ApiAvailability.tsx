import TryItForm from "./TryItForm";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function ApiAvailability() {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-8 shadow-glow">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">API Availability</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-white/75">
            Run the FastAPI service locally and test via Swagger.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <a
            href={`${apiBase}/docs`}
            className="rounded-xl border border-white/15 bg-white/10 px-4 py-2 text-sm hover:bg-white/15"
          >
            Swagger docs
          </a>
          <a
            href={`${apiBase}/health`}
            className="rounded-xl border border-white/15 bg-white/10 px-4 py-2 text-sm hover:bg-white/15"
          >
            Health check
          </a>
        </div>
      </div>

      <div className="mt-8 grid gap-4 md:grid-cols-2">
        <Endpoint
          method="POST"
          path="/predict"
          desc="Classify one job posting and return explainable reasons."
        />
        <Endpoint
          method="POST"
          path="/batch-predict"
          desc="Classify many job postings in a single request."
        />
        <Endpoint method="GET" path="/health" desc="Service status." />
      </div>

      <div className="mt-8">
        <TryItForm />
      </div>
    </div>
  );
}

function Endpoint({
  method,
  path,
  desc,
}: {
  method: "GET" | "POST";
  path: string;
  desc: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <div className="flex items-center gap-2">
        <span className="rounded-lg border border-indigo-500/40 bg-indigo-500/15 px-2 py-1 text-xs font-semibold">
          {method}
        </span>
        <span className="font-mono text-sm">{path}</span>
      </div>
      <p className="mt-2 text-sm leading-6 text-white/75">{desc}</p>
    </div>
  );
}
