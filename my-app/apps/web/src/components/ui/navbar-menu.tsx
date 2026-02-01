import type { ReactNode } from "react";

export function Menu({ children }: { children: ReactNode }) {
  return <nav aria-label="Menu">{children}</nav>;
}

export function MenuItem({ children }: { children: ReactNode }) {
  return <div>{children}</div>;
}

export function HoveredLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a href={href} className="text-sm text-white/80 hover:text-white">
      {children}
    </a>
  );
}

export function ProductItem({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-3">
      <div className="text-sm font-semibold">{title}</div>
      <div className="mt-1 text-xs text-white/70">{description}</div>
    </div>
  );
}
