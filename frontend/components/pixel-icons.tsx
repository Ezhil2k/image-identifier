import React from "react";

export function PixelRefresh({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="16" height="16" rx="2" fill="#fff" stroke="#222" strokeWidth="2" />
      <path d="M6 10h4V6h2v6H6v-2z" fill="#222" />
      <rect x="9" y="3" width="2" height="2" fill="#222" />
      <rect x="15" y="9" width="2" height="2" fill="#222" />
    </svg>
  );
}

export function PixelSun({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="16" height="16" rx="2" fill="#fff" stroke="#222" strokeWidth="2" />
      <rect x="8" y="8" width="4" height="4" fill="#222" />
      <rect x="9" y="4" width="2" height="2" fill="#222" />
      <rect x="9" y="14" width="2" height="2" fill="#222" />
      <rect x="4" y="9" width="2" height="2" fill="#222" />
      <rect x="14" y="9" width="2" height="2" fill="#222" />
    </svg>
  );
}

export function PixelMoon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="16" height="16" rx="2" fill="#fff" stroke="#222" strokeWidth="2" />
      <rect x="8" y="7" width="4" height="6" fill="#222" />
      <rect x="10" y="5" width="2" height="2" fill="#222" />
      <rect x="10" y="13" width="2" height="2" fill="#222" />
    </svg>
  );
} 