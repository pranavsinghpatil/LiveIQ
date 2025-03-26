import { ChangeEvent } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

interface Platform {
  id: string;
  name: string;
}

interface SearchBarProps {
  searchTerm: string;
  onSearch: (term: string) => void;
  onPlatformChange: (platform: string | null) => void;
  selectedPlatform: string | null;
  platforms: Platform[];
}

export const SearchBar = ({
  searchTerm,
  onSearch,
  onPlatformChange,
  selectedPlatform,
  platforms
}: SearchBarProps) => {
  const handleSearchChange = (e: ChangeEvent<HTMLInputElement>) => {
    onSearch(e.target.value);
  };

  const handlePlatformChange = (e: ChangeEvent<HTMLSelectElement>) => {
    onPlatformChange(e.target.value || null);
  };

  return (
    <div className="flex gap-4 p-4 bg-background border-b border-primary/20">
      <div className="flex-1 relative">
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-text/40" />
        <input
          type="text"
          placeholder="Search chats..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="w-full pl-10 pr-4 py-2 bg-background-dark border border-primary/30 rounded-lg text-text placeholder-text/40 focus:outline-none focus:ring-2 focus:ring-primary/50"
        />
      </div>
      <select
        value={selectedPlatform || ''}
        onChange={handlePlatformChange}
        className="px-4 py-2 bg-background-dark border border-primary/30 rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-primary/50"
      >
        <option value="">All Platforms</option>
        {platforms.map(platform => (
          <option key={platform.id} value={platform.id} className="bg-background-dark text-text">
            {platform.name}
          </option>
        ))}
      </select>
    </div>
  );
};
