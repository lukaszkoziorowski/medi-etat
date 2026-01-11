'use client';

interface FilterPillProps {
  label: string;
  isSelected: boolean;
  onClick: () => void;
}

export default function FilterPill({ label, isSelected, onClick }: FilterPillProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        px-4 py-2 rounded-full text-sm font-medium transition-all duration-200
        ${
          isSelected
            ? 'bg-[#1a1a1a] text-white border-2 border-[#1a1a1a] hover:bg-[#2a2a2a]'
            : 'bg-white text-gray-700 border-2 border-gray-200 hover:border-gray-300 hover:bg-gray-50'
        }
        focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:ring-offset-2
      `}
    >
      {label}
    </button>
  );
}
