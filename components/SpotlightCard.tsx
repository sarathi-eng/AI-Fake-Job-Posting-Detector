"use client";

import type { HTMLAttributes } from "react";
import { useRef } from "react";

import { cn } from "../lib/utils";

type Props = HTMLAttributes<HTMLDivElement> & {
  spotlightColor?: string;
};

export default function SpotlightCard({
  className,
  children,
  spotlightColor = "rgba(99, 102, 241, 0.25)",
  ...props
}: Props) {
  const ref = useRef<HTMLDivElement | null>(null);

  function onMove(e: React.MouseEvent<HTMLDivElement>) {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    el.style.setProperty("--spotlight-x", `${x}px`);
    el.style.setProperty("--spotlight-y", `${y}px`);
    el.style.setProperty("--spotlight-color", spotlightColor);
  }

  function onLeave() {
    const el = ref.current;
    if (!el) return;
    el.style.removeProperty("--spotlight-x");
    el.style.removeProperty("--spotlight-y");
  }

  return (
    <div
      ref={ref}
      onMouseMove={onMove}
      onMouseLeave={onLeave}
      className={cn(
        "group relative overflow-hidden rounded-2xl",
        "border border-white/10 bg-white/5",
        "shadow-glow",
        "transition-colors",
        className
      )}
      {...props}
    >
      <div
        aria-hidden="true"
        className={cn(
          "pointer-events-none absolute inset-0 opacity-0",
          "transition-opacity duration-200 group-hover:opacity-100"
        )}
        style={{
          background:
            "radial-gradient(520px circle at var(--spotlight-x, -999px) var(--spotlight-y, -999px), var(--spotlight-color, rgba(99, 102, 241, 0.15)), transparent 55%)",
        }}
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-gradient-to-b from-white/8 to-transparent opacity-40"
      />
      <div className="relative">{children}</div>
    </div>
  );
}
