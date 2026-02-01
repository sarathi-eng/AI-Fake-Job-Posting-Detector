import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          950: "#070A12",
          900: "#0B1020",
          800: "#0F1730",
        },
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(255,255,255,0.08), 0 12px 40px rgba(0,0,0,0.55)",
      },
      keyframes: {
        shimmer: {
          "0%": { transform: "translateX(-50%)" },
          "100%": { transform: "translateX(50%)" },
        },
      },
      animation: {
        shimmer: "shimmer 3s linear infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
