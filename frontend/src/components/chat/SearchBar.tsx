import { ChangeEvent } from 'react';

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
    <div className="flex gap-4 p-4">
      <input
        type="text"
        placeholder="Search chats..."
        value={searchTerm}
        onChange={handleSearchChange}
        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <select
        value={selectedPlatform || ''}
        onChange={handlePlatformChange}
        className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Platforms</option>
        {platforms.map(platform => (
          <option key={platform.id} value={platform.id}>
            {platform.name}
          </option>
        ))}
      </select>
    </div>
  );
};
