import { cn } from "../lib/utils";
import { HoveredLink, Menu, MenuItem, ProductItem } from "./ui/navbar-menu";

export default function Navigation() {
  return (
    <div className={cn("rounded-2xl border border-white/10 bg-white/5 p-4")}
    >
      <Menu>
        <MenuItem>
          <div className="flex gap-4">
            <HoveredLink href="#">Home</HoveredLink>
            <HoveredLink href="#">Features</HoveredLink>
          </div>
        </MenuItem>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <ProductItem title="Text Analysis" description="Flags scam patterns." />
          <ProductItem title="Explainable Output" description="Reasons + confidence." />
        </div>
      </Menu>
    </div>
  );
}
