import { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

interface Platform {
  id: string;
  name: string;
}

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onPlatformChange: (platform: string | null) => void;
  platforms: Platform[];
}

export const SearchBar = ({ value, onChange, onPlatformChange, platforms }: SearchBarProps) => {
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);

  const handlePlatformChange = (platformId: string) => {
    const newPlatform = selectedPlatform === platformId ? null : platformId;
    setSelectedPlatform(newPlatform);
    onPlatformChange(newPlatform);
  };

  return (
    <div className="space-y-4">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          placeholder="Search across all AI platforms..."
        />
      </div>

      <div className="flex flex-wrap gap-2">
        {platforms.map((platform) => (
          <button
            key={platform.id}
            onClick={() => handlePlatformChange(platform.id)}
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
              selectedPlatform === platform.id
                ? 'bg-primary-100 text-primary-800'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            {platform.name}
          </button>
        ))}
      </div>
    </div>
  );
};
