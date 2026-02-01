"use client";

import { useEffect, useMemo, useState } from "react";

type Props = {
  text: string;
  speedMs?: number;
  startDelayMs?: number;
};

export default function TypewriterText({
  text,
  speedMs = 18,
  startDelayMs = 120,
}: Props) {
  const characters = useMemo(() => Array.from(text), [text]);
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(0);

    const startTimer = window.setTimeout(() => {
      const interval = window.setInterval(() => {
        setCount((prev) => {
          const next = prev + 1;
          if (next >= characters.length) {
            window.clearInterval(interval);
            return characters.length;
          }
          return next;
        });
      }, speedMs);
    }, startDelayMs);

    return () => {
      window.clearTimeout(startTimer);
    };
  }, [characters.length, speedMs, startDelayMs]);

  const visible = characters.slice(0, count).join("");

  return (
    <span className="relative">
      <span>{visible}</span>
      <span
        aria-hidden="true"
        className="ml-[2px] inline-block h-[1em] w-[2px] translate-y-[2px] animate-pulse bg-white/70"
      />
    </span>
  );
}
