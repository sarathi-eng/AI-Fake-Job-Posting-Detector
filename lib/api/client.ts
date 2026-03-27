type PredictPayload = {
  title: string;
  company_name: string;
  description: string;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
};

export async function predictJob(payload: PredictPayload) {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  const response = await fetch(`${base}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}
