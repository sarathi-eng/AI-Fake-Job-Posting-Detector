import { CardStack } from "./ui/card-stack";
import { cn } from "../lib/utils";

export default function CardStackDemo() {
  return (
    <div className={cn("rounded-2xl border border-white/10 bg-white/5 p-6")}
    >
      <div className="text-sm font-semibold">Card Stack Demo</div>
      <CardStack>
        <div className="rounded-xl border border-white/10 bg-bg-900/40 p-3 text-sm text-white/80">
          Sample card 1
        </div>
        <div className="rounded-xl border border-white/10 bg-bg-900/40 p-3 text-sm text-white/80">
          Sample card 2
        </div>
      </CardStack>
    </div>
  );
}
