import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

