import * as React from "react";

import { cn } from "../../lib/utils";

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "secondary" | "ghost";
};

export function Button({ className, variant = "default", ...props }: ButtonProps) {
  const base =
    "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black disabled:pointer-events-none disabled:opacity-50";

  const variants: Record<NonNullable<ButtonProps["variant"]>, string> = {
    default: "bg-black text-white hover:bg-black/90 h-10 px-4 py-2",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 h-10 px-4 py-2",
    ghost: "hover:bg-gray-100 text-gray-900 h-10 px-4 py-2"
  };

  return <button className={cn(base, variants[variant], className)} {...props} />;
}
