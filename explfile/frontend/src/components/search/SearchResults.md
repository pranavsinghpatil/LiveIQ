# SearchResults Component Documentation

## Overview
The SearchResults component displays search results from chat queries, providing a rich interface for viewing and interacting with matched messages and conversations.

## Component Implementation

### Component Structure
```typescript
interface SearchResultsProps {
  results: SearchResult[];
  isLoading?: boolean;
  onResultClick?: (result: SearchResult) => void;
  onClearResults?: () => void;
  emptyStateMessage?: string;
}

const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  isLoading = false,
  onResultClick,
  onClearResults,
  emptyStateMessage = 'No results found'
}) => {
  const [selectedResult, setSelectedResult] = useState<string | null>(null);
  
  // Handle result selection
  const handleResultClick = (result: SearchResult) => {
    setSelectedResult(result.id);
    onResultClick?.(result);
  };
  
  // Clear results
  const handleClear = () => {
    setSelectedResult(null);
    onClearResults?.();
  };
  
  // Render loading state
  if (isLoading) {
    return (
      <div className="search-results-loading">
        <LoadingSpinner size="md" />
        <p>Searching conversations...</p>
      </div>
    );
  }
  
  // Render empty state
  if (results.length === 0) {
    return (
      <div className="search-results-empty">
        <SearchEmptyIcon />
        <p>{emptyStateMessage}</p>
      </div>
    );
  }
  
  return (
    <div className="search-results">
      <div className="search-results-header">
        <h3>Search Results ({results.length})</h3>
        <button
          className="clear-results-btn"
          onClick={handleClear}
        >
          Clear
        </button>
      </div>
      
      <div className="search-results-list">
        {results.map((result) => (
          <SearchResultItem
            key={result.id}
            result={result}
            isSelected={selectedResult === result.id}
            onClick={() => handleResultClick(result)}
          />
        ))}
      </div>
    </div>
  );
};
```

### SearchResultItem Component
```typescript
interface SearchResultItemProps {
  result: SearchResult;
  isSelected?: boolean;
  onClick?: () => void;
}

const SearchResultItem: React.FC<SearchResultItemProps> = ({
  result,
  isSelected = false,
  onClick
}) => {
  // Format date for display
  const formattedDate = useMemo(() => {
    return formatDate(result.timestamp);
  }, [result.timestamp]);
  
  // Highlight matched text
  const highlightMatches = (text: string, matches: string[]) => {
    if (!matches.length) return text;
    
    let highlightedText = text;
    matches.forEach((match) => {
      const regex = new RegExp(`(${escapeRegExp(match)})`, 'gi');
      highlightedText = highlightedText.replace(
        regex,
        '<span class="highlight">$1</span>'
      );
    });
    
    return highlightedText;
  };
  
  return (
    <div
      className={clsx('search-result-item', {
        'selected': isSelected
      })}
      onClick={onClick}
    >
      <div className="result-header">
        <div className="chat-info">
          <h4>{result.chatTitle}</h4>
          <span className="platform-badge">
            {result.platform}
          </span>
        </div>
        
        <div className="result-meta">
          <span className="result-date">{formattedDate}</span>
          {result.tags?.length > 0 && (
            <div className="result-tags">
              {result.tags.map((tag) => (
                <span key={tag} className="tag">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
      
      <div className="result-content">
        <p
          dangerouslySetInnerHTML={{
            __html: highlightMatches(
              result.content,
              result.matches || []
            )
          }}
        />
      </div>
      
      {result.contextBefore && (
        <div className="result-context before">
          <button
            className="context-toggle"
            onClick={(e) => {
              e.stopPropagation();
              // Toggle context visibility
            }}
          >
            Show previous messages
          </button>
        </div>
      )}
      
      {result.contextAfter && (
        <div className="result-context after">
          <button
            className="context-toggle"
            onClick={(e) => {
              e.stopPropagation();
              // Toggle context visibility
            }}
          >
            Show following messages
          </button>
        </div>
      )}
    </div>
  );
};
```

## Styling

### CSS Modules
```scss
.search-results {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--color-background);
  
  .search-results-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid var(--color-border);
    
    h3 {
      margin: 0;
      font-size: 1rem;
      font-weight: 500;
      color: var(--color-text);
    }
    
    .clear-results-btn {
      padding: 0.25rem 0.5rem;
      background: transparent;
      border: none;
      color: var(--color-text-secondary);
      font-size: 0.875rem;
      cursor: pointer;
      
      &:hover {
        color: var(--color-primary);
      }
    }
  }
  
  .search-results-list {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
    
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .search-results-loading,
  .search-results-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 2rem;
    
    svg {
      width: 3rem;
      height: 3rem;
      color: var(--color-text-secondary);
      margin-bottom: 1rem;
    }
    
    p {
      margin: 0;
      color: var(--color-text-secondary);
      font-size: 0.875rem;
      text-align: center;
    }
  }
  
  .search-result-item {
    padding: 1rem;
    border-radius: 0.5rem;
    background: var(--color-background-dark);
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      background: var(--color-background-dark);
      transform: translateY(-1px);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    &.selected {
      background: var(--color-primary/10);
      border: 1px solid var(--color-primary/30);
    }
    
    .result-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 0.5rem;
      
      .chat-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        
        h4 {
          margin: 0;
          font-size: 0.875rem;
          font-weight: 500;
          color: var(--color-text);
        }
        
        .platform-badge {
          padding: 0.125rem 0.375rem;
          border-radius: 9999px;
          background: var(--color-primary);
          color: white;
          font-size: 0.625rem;
          text-transform: uppercase;
        }
      }
      
      .result-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.25rem;
        
        .result-date {
          font-size: 0.75rem;
          color: var(--color-text-secondary);
        }
        
        .result-tags {
          display: flex;
          gap: 0.25rem;
          
          .tag {
            padding: 0.125rem 0.375rem;
            border-radius: 9999px;
            background: var(--color-background);
            color: var(--color-text-secondary);
            font-size: 0.625rem;
          }
        }
      }
    }
    
    .result-content {
      margin-bottom: 0.5rem;
      
      p {
        margin: 0;
        font-size: 0.875rem;
        line-height: 1.5;
        color: var(--color-text);
        
        .highlight {
          background: var(--color-primary/20);
          color: var(--color-primary);
          padding: 0 0.125rem;
          border-radius: 0.125rem;
          font-weight: 500;
        }
      }
    }
    
    .result-context {
      padding: 0.25rem 0;
      
      &.before {
        border-top: 1px dashed var(--color-border);
        margin-top: 0.5rem;
      }
      
      &.after {
        border-bottom: 1px dashed var(--color-border);
        margin-bottom: 0.5rem;
      }
      
      .context-toggle {
        background: transparent;
        border: none;
        color: var(--color-primary);
        font-size: 0.75rem;
        cursor: pointer;
        padding: 0;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}
```

## Usage Examples

### Basic Usage
```typescript
function SearchPage() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSearch = async (query: string, filters: SearchFilters) => {
    if (!query) {
      setResults([]);
      return;
    }
    
    setIsLoading(true);
    
    try {
      const response = await api.get('/search', {
        params: {
          query,
          ...filters
        }
      });
      
      setResults(response.data.results);
    } catch (error) {
      console.error('Search error:', error);
      toast.error('Failed to search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleResultClick = (result: SearchResult) => {
    navigate(`/chats/${result.chatId}?messageId=${result.id}`);
  };
  
  return (
    <div className="search-page">
      <SearchBar onSearch={handleSearch} />
      
      <SearchResults
        results={results}
        isLoading={isLoading}
        onResultClick={handleResultClick}
        onClearResults={() => setResults([])}
      />
    </div>
  );
}
```

### With Custom Empty State
```typescript
function EmptySearchResults() {
  return (
    <SearchResults
      results={[]}
      emptyStateMessage={
        <div className="custom-empty-state">
          <p>No results found for your search.</p>
          <p>Try adjusting your search terms or filters.</p>
          <button>View Search Tips</button>
        </div>
      }
    />
  );
}
```

### With Result Grouping
```typescript
function GroupedSearchResults() {
  const [results, setResults] = useState<SearchResult[]>([]);
  
  // Group results by chat
  const groupedResults = useMemo(() => {
    const groups: Record<string, SearchResult[]> = {};
    
    results.forEach((result) => {
      if (!groups[result.chatId]) {
        groups[result.chatId] = [];
      }
      
      groups[result.chatId].push(result);
    });
    
    return groups;
  }, [results]);
  
  return (
    <div className="grouped-search-results">
      {Object.entries(groupedResults).map(([chatId, chatResults]) => (
        <div key={chatId} className="chat-results-group">
          <h3>{chatResults[0].chatTitle}</h3>
          
          <SearchResults
            results={chatResults}
            onResultClick={handleResultClick}
          />
        </div>
      ))}
    </div>
  );
}
```

## Type Definitions

```typescript
interface SearchResult {
  id: string;
  chatId: string;
  chatTitle: string;
  content: string;
  sender: string;
  timestamp: string;
  platform: string;
  matches?: string[];
  tags?: string[];
  contextBefore?: boolean;
  contextAfter?: boolean;
}

interface SearchFilters {
  platform?: string;
  dateRange?: {
    start: string;
    end: string;
  };
  tags?: string[];
  contentType?: 'text' | 'code' | 'media';
}
```

## Error Handling

```typescript
const handleSearchError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    const response = error.response;
    
    if (response?.status === 400) {
      return 'Invalid search query. Please try different search terms.';
    }
    
    if (response?.status === 401) {
      return 'Please log in to search your conversations.';
    }
    
    if (response?.status === 429) {
      return 'Too many search requests. Please try again later.';
    }
    
    return 'Failed to search. Please try again.';
  }
  
  return 'An unexpected error occurred. Please try again.';
};
```
