import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const convertSize = (kb: number) => {
  const mb = kb / 1024; // 1 MB = 1024 KB
  const gb = mb / 1024; // 1 GB = 1024 MB
  
  // If size is greater than 500MB, return in GB
  if (mb > 500) {
    return gb.toFixed() + " GB";
  } else {
    return  mb.toFixed(2) + " MB"
  }
};