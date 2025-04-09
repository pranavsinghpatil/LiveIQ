import { ButtonHTMLAttributes } from "react";
import { cn } from "../../utils/cn";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline";
  size?: "sm" | "md" | "lg";
}

export const Button = ({
  className,
  variant = "primary",
  size = "md",
  ...props
}: ButtonProps) => {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        {
          "bg-primary hover:bg-primary-dark text-white": variant === "primary",
          "bg-gray-100 hover:bg-gray-200 text-gray-900": variant === "secondary",
          "border border-gray-300 bg-transparent hover:bg-gray-100": variant === "outline",
        },
        {
          "h-8 px-3 text-sm": size === "sm",
          "h-10 px-4 text-base": size === "md",
          "h-12 px-6 text-lg": size === "lg",
        },
        className
      )}
      {...props}
    />
  );
};
