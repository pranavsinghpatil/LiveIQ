import { HTMLAttributes } from "react";
import { cn } from "../../utils/cn";

interface CardProps extends HTMLAttributes<HTMLDivElement> {}

export const Card = ({ className, ...props }: CardProps) => {
  return (
    <div
      className={cn(
        "rounded-lg bg-white shadow-md dark:bg-gray-800",
        className
      )}
      {...props}
    />
  );
};
