interface ForeheadFrownIconProps {
  className?: string;
}

export function ForeheadFrownIcon({ className = "w-6 h-6" }: ForeheadFrownIconProps) {
  return (
    <svg 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round"
      className={className}
    >
      {/* Face circle */}
      <circle cx="12" cy="12" r="10" />
      
      {/* Left eye */}
      <circle cx="9" cy="11" r="1.5" fill="currentColor" />
      
      {/* Right eye */}
      <circle cx="15" cy="11" r="1.5" fill="currentColor" />
      
      {/* Neutral/slight frown mouth */}
      <path d="M8 16.5 Q12 15.5 16 16.5" />
      
      {/* Forehead furrow lines - concentration wrinkles */}
      <path d="M7 7 L8.5 8" strokeWidth="1.5" />
      <path d="M10 6.5 L11 7.5" strokeWidth="1.5" />
      <path d="M13 6.5 L14 7.5" strokeWidth="1.5" />
      <path d="M16 7 L17 8" strokeWidth="1.5" />
      
      {/* Diagonal worry lines between eyebrows */}
      <path d="M10.5 8.5 L11.5 9.5" strokeWidth="1.5" />
      <path d="M13.5 8.5 L12.5 9.5" strokeWidth="1.5" />
    </svg>
  );
}
