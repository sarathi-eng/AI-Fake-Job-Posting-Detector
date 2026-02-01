import { cn } from "../lib/utils";
import ShinyButton from "./ShinyButton";

const links = [
  { href: "#home", label: "Home" },
  { href: "#features", label: "Features" },
  { href: "#demo", label: "API" },
  { href: "#follow", label: "Follow" },
] as const;

export default function Navbar() {
  return (
    <div className="fixed top-4 left-0 right-0 z-50">
      <div className="mx-auto w-full max-w-6xl px-6">
        <nav
          className={cn(
            "flex items-center justify-between gap-4 rounded-2xl",
            "border border-white/10 bg-bg-900/60",
            "px-4 py-3 backdrop-blur shadow-glow"
          )}
          aria-label="Primary"
        >
          <a
            href="#home"
            className="text-sm font-semibold tracking-tight hover:text-white/90"
          >
            Fake Job Detector
          </a>

          <div className="hidden items-center gap-1 md:flex">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className={cn(
                  "rounded-xl px-3 py-2 text-sm text-white/75",
                  "hover:bg-white/10 hover:text-white"
                )}
              >
                {link.label}
              </a>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <ShinyButton href="#demo" variant="primary" className="px-3 py-2">
              API Access
            </ShinyButton>
          </div>
        </nav>
      </div>
    </div>
  );
}
