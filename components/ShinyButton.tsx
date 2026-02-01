import type { AnchorHTMLAttributes } from "react";

import { cn } from "../lib/utils";

type Props = AnchorHTMLAttributes<HTMLAnchorElement> & {
  variant?: "primary" | "secondary";
};

export default function ShinyButton({
  variant = "secondary",
  className,
  children,
  ...props
}: Props) {
  return (
    <a
      className={cn(
        "relative inline-flex items-center justify-center",
        "overflow-hidden rounded-xl px-4 py-2",
        "text-sm font-medium",
        "transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400/60",
        "focus-visible:ring-offset-2 focus-visible:ring-offset-bg-950",
        variant === "primary"
          ? "border border-indigo-500/45 bg-indigo-500/15 text-white hover:bg-indigo-500/20"
          : "border border-white/15 bg-white/10 text-white/90 hover:bg-white/15",
        "before:pointer-events-none before:absolute before:inset-0",
        "before:-translate-x-full",
        "before:bg-[linear-gradient(115deg,transparent,rgba(255,255,255,0.22),transparent)]",
        "before:animate-shimmer before:content-['']",
        className
      )}
      {...props}
    >
      <span className="relative inline-flex items-center gap-2">{children}</span>
    </a>
  );
}
