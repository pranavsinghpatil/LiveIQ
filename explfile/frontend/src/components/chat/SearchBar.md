# SearchBar Component

## Purpose
The SearchBar component provides a unified search interface for VoxStitch, allowing users to search through their chat history with advanced filtering options.

## Component Structure

### Main Component
```typescript
interface SearchBarProps {
  onSearch: (query: string) => void;
  onFilterChange: (filters: SearchFilters) => void;
  placeholder?: string;
  initialQuery?: string;
  className?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  onFilterChange,
  placeholder = 'Search chats...',
  initialQuery = '',
  className
}) => {
  // Component implementation
};
```

## Features

### 1. Search Input
```typescript
const SearchInput: React.FC<{
  value: string;
  onChange: (value: string) => void;
}> = ({ value, onChange }) => {
  return (
    <div className="relative flex-1">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={clsx(
          'w-full px-4 py-2 rounded-lg',
          'bg-gradient-to-b from-surface-100 to-surface-200',
          'border border-primary/20',
          'focus:outline-none focus:ring-2 focus:ring-primary/30',
          'placeholder-gray-400'
        )}
        placeholder="Search chats..."
      />
      <SearchIcon className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
    </div>
  );
};
```

### 2. Advanced Filters
```typescript
interface SearchFilters {
  platform?: string;
  dateRange?: DateRange;
  tags?: string[];
  contentType?: 'text' | 'code' | 'media';
}

const FilterPanel: React.FC<{
  filters: SearchFilters;
  onChange: (filters: SearchFilters) => void;
}> = ({ filters, onChange }) => {
  return (
    <div className="p-4 bg-gradient-to-b from-surface-50 to-surface-100 rounded-lg">
      <PlatformFilter
        value={filters.platform}
        onChange={(platform) => onChange({ ...filters, platform })}
      />
      <DateRangeFilter
        value={filters.dateRange}
        onChange={(dateRange) => onChange({ ...filters, dateRange })}
      />
      <TagFilter
        value={filters.tags}
        onChange={(tags) => onChange({ ...filters, tags })}
      />
    </div>
  );
};
```

### 3. Search Suggestions
```typescript
const SearchSuggestions: React.FC<{
  query: string;
  onSelect: (suggestion: string) => void;
}> = ({ query, onSelect }) => {
  const suggestions = useMemo(() => {
    return generateSuggestions(query);
  }, [query]);

  return (
    <div className="absolute top-full left-0 right-0 mt-2 bg-surface-100 rounded-lg shadow-lg">
      {suggestions.map((suggestion) => (
        <button
          key={suggestion}
          className={clsx(
            'w-full px-4 py-2 text-left',
            'hover:bg-gradient-to-r hover:from-primary-500/10 hover:to-primary-600/10'
          )}
          onClick={() => onSelect(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
};
```

## State Management

### Search State
```typescript
const [query, setQuery] = useState(initialQuery);
const [filters, setFilters] = useState<SearchFilters>({});
const [showSuggestions, setShowSuggestions] = useState(false);

const debouncedSearch = useCallback(
  debounce((term: string) => {
    onSearch(term);
  }, 300),
  [onSearch]
);

useEffect(() => {
  debouncedSearch(query);
}, [query, debouncedSearch]);
```

### Filter State
```typescript
const [isFilterPanelOpen, setIsFilterPanelOpen] = useState(false);

const handleFilterChange = (newFilters: SearchFilters) => {
  setFilters(newFilters);
  onFilterChange(newFilters);
};
```

## UI/UX Features

### 1. Loading State
```typescript
const LoadingIndicator: React.FC = () => (
  <div className="absolute right-12 top-1/2 transform -translate-y-1/2">
    <div className="w-4 h-4 border-2 border-primary/30 border-t-primary rounded-full animate-spin" />
  </div>
);
```

### 2. Clear Button
```typescript
const ClearButton: React.FC<{
  onClick: () => void;
}> = ({ onClick }) => (
  <button
    className={clsx(
      'absolute right-12 top-1/2 transform -translate-y-1/2',
      'text-gray-400 hover:text-gray-600 transition-colors'
    )}
    onClick={onClick}
  >
    <XIcon className="w-4 h-4" />
  </button>
);
```

### 3. Filter Toggle
```typescript
const FilterToggle: React.FC<{
  isOpen: boolean;
  onClick: () => void;
}> = ({ isOpen, onClick }) => (
  <button
    className={clsx(
      'ml-2 p-2 rounded-lg',
      'bg-gradient-to-r from-primary-500 to-primary-600',
      'text-white hover:from-primary-600 hover:to-primary-700',
      'transition-colors'
    )}
    onClick={onClick}
  >
    <FilterIcon className="w-5 h-5" />
  </button>
);
```

## Performance Optimizations

### 1. Debounced Search
```typescript
const debouncedSearch = useCallback(
  debounce((term: string) => {
    onSearch(term);
  }, 300),
  [onSearch]
);
```

### 2. Memoized Suggestions
```typescript
const suggestions = useMemo(() => {
  if (!query || query.length < 2) return [];
  return generateSuggestions(query);
}, [query]);
```

## Integration Points

### API Integration
```typescript
const fetchSuggestions = async (query: string) => {
  try {
    const response = await api.get(`/search/suggestions?q=${query}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch suggestions:', error);
    return [];
  }
};
```

### Event Handling
```typescript
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    setShowSuggestions(false);
  }
};
```

## Related Components
- `ChatList`: Displays filtered results
- `FilterPanel`: Advanced filtering options
- `TagInput`: Tag selection component
- `DatePicker`: Date range selection

## Testing
```typescript
describe('SearchBar', () => {
  it('debounces search correctly', () => {
    jest.useFakeTimers();
    const onSearch = jest.fn();
    const { getByRole } = render(<SearchBar onSearch={onSearch} />);
    
    fireEvent.change(getByRole('textbox'), { target: { value: 'test' } });
    expect(onSearch).not.toHaveBeenCalled();
    
    jest.runAllTimers();
    expect(onSearch).toHaveBeenCalledWith('test');
  });
});
```

## Recent Updates
- Added gradient styling
- Improved suggestion algorithm
- Enhanced filter panel UI
- Added keyboard navigation
- Improved accessibility

## Accessibility Features
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- High contrast mode support
