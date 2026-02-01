export default function Footer() {
  const githubUrl =
    process.env.NEXT_PUBLIC_GITHUB_URL ?? "https://github.com/sarathi-eng";
  const instagramUrl =
    process.env.NEXT_PUBLIC_INSTAGRAM_URL ??
    "https://instagram.com/navilor_";

  return (
    <footer id="follow" className="border-t border-white/10">
      <div className="mx-auto w-full max-w-6xl px-6 py-12">
        <div className="grid gap-8 md:grid-cols-2">
          <div>
            <div className="text-sm font-semibold">Developed by Sarathi S</div>
            <p className="mt-2 text-sm leading-6 text-white/70">
              Links:
            </p>

            <div className="mt-4 flex items-center gap-3">
              <SocialIconLink
                href={instagramUrl}
                label="Instagram"
                icon={<InstagramIcon />}
              />
              <SocialIconLink
                href={githubUrl}
                label="GitHub"
                icon={<GitHubIcon />}
              />
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-glow">
            <div className="text-sm font-semibold">Integrate anywhere</div>
            <p className="mt-2 text-sm leading-6 text-white/70">
              Use the API behind a job board, ATS ingestion, internal trust &
              safety tooling, or a browser extension backend.
            </p>
            <p className="mt-4 text-xs text-white/55">
              © {new Date().getFullYear()} Fake Job Posting Detector
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

function SocialIconLink({
  href,
  label,
  icon,
}: {
  href: string;
  label: string;
  icon: React.ReactNode;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      aria-label={label}
      title={label}
      className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-white/15 bg-white/10 text-white/80 transition-colors hover:bg-white/15 hover:text-white"
    >
      {icon}
    </a>
  );
}

function InstagramIcon() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      className="h-5 w-5"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="3" y="3" width="18" height="18" rx="5" />
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37Z" />
      <path d="M17.5 6.5h.01" />
    </svg>
  );
}

function GitHubIcon() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      className="h-5 w-5"
      fill="currentColor"
    >
      <path d="M12 2C6.48 2 2 6.58 2 12.23c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.48 0-.24-.01-.87-.01-1.7-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.11-1.5-1.11-1.5-.9-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.89 1.57 2.34 1.12 2.91.86.09-.67.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.08 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.32.1-2.76 0 0 .84-.27 2.75 1.05.8-.23 1.66-.34 2.51-.35.85.01 1.71.12 2.51.35 1.91-1.32 2.75-1.05 2.75-1.05.55 1.44.2 2.5.1 2.76.64.72 1.03 1.63 1.03 2.75 0 3.95-2.34 4.81-4.57 5.07.36.32.68.95.68 1.92 0 1.39-.01 2.51-.01 2.85 0 .27.18.59.69.48A10.2 10.2 0 0 0 22 12.23C22 6.58 17.52 2 12 2Z" />
    </svg>
  );
}
