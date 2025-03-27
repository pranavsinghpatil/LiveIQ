# SearchBar Component Tests

## Purpose
Test suite for the SearchBar component, which provides advanced search functionality for chat conversations with filtering and sorting capabilities.

## Test Structure

### 1. Basic Search Tests
```typescript
describe('SearchBar Basic Search', () => {
  it('renders search input correctly', () => {
    const { getByPlaceholderText } = render(<SearchBar />);
    
    expect(getByPlaceholderText('Search chats...')).toBeInTheDocument();
  });

  it('handles search input changes', () => {
    const onSearch = jest.fn();
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={onSearch} />
    );
    
    const input = getByPlaceholderText('Search chats...');
    fireEvent.change(input, {
      target: { value: 'test query' }
    });
    
    expect(onSearch).toHaveBeenCalledWith('test query');
  });

  it('debounces search input', async () => {
    const onSearch = jest.fn();
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={onSearch} debounceMs={300} />
    );
    
    const input = getByPlaceholderText('Search chats...');
    
    // Type quickly
    fireEvent.change(input, { target: { value: 't' } });
    fireEvent.change(input, { target: { value: 'te' } });
    fireEvent.change(input, { target: { value: 'tes' } });
    fireEvent.change(input, { target: { value: 'test' } });
    
    // Should not call immediately
    expect(onSearch).not.toHaveBeenCalled();
    
    // Should call after debounce
    await waitFor(() => {
      expect(onSearch).toHaveBeenCalledWith('test');
      expect(onSearch).toHaveBeenCalledTimes(1);
    });
  });
});
```

### 2. Filter Tests
```typescript
describe('SearchBar Filters', () => {
  it('renders filter options correctly', () => {
    const { getByText } = render(<SearchBar />);
    
    expect(getByText('Platform')).toBeInTheDocument();
    expect(getByText('Date')).toBeInTheDocument();
    expect(getByText('Status')).toBeInTheDocument();
  });

  it('handles platform filter selection', () => {
    const onFilterChange = jest.fn();
    const { getByText } = render(
      <SearchBar onFilterChange={onFilterChange} />
    );
    
    fireEvent.click(getByText('Platform'));
    fireEvent.click(getByText('ChatGPT'));
    
    expect(onFilterChange).toHaveBeenCalledWith({
      platform: 'chatgpt'
    });
  });

  it('handles date range filter', () => {
    const onFilterChange = jest.fn();
    const { getByText, getByLabelText } = render(
      <SearchBar onFilterChange={onFilterChange} />
    );
    
    fireEvent.click(getByText('Date'));
    
    const startDate = getByLabelText('Start date');
    const endDate = getByLabelText('End date');
    
    fireEvent.change(startDate, {
      target: { value: '2024-03-01' }
    });
    fireEvent.change(endDate, {
      target: { value: '2024-03-31' }
    });
    
    expect(onFilterChange).toHaveBeenCalledWith({
      dateRange: {
        start: '2024-03-01',
        end: '2024-03-31'
      }
    });
  });

  it('handles status filter selection', () => {
    const onFilterChange = jest.fn();
    const { getByText } = render(
      <SearchBar onFilterChange={onFilterChange} />
    );
    
    fireEvent.click(getByText('Status'));
    fireEvent.click(getByText('Processed'));
    
    expect(onFilterChange).toHaveBeenCalledWith({
      status: 'processed'
    });
  });
});
```

### 3. Sort Tests
```typescript
describe('SearchBar Sorting', () => {
  it('renders sort options correctly', () => {
    const { getByText } = render(<SearchBar />);
    
    expect(getByText('Sort by')).toBeInTheDocument();
    expect(getByText('Date')).toBeInTheDocument();
    expect(getByText('Name')).toBeInTheDocument();
  });

  it('handles sort selection', () => {
    const onSortChange = jest.fn();
    const { getByText } = render(
      <SearchBar onSortChange={onSortChange} />
    );
    
    fireEvent.click(getByText('Sort by'));
    fireEvent.click(getByText('Date'));
    
    expect(onSortChange).toHaveBeenCalledWith({
      field: 'date',
      direction: 'desc'
    });
  });

  it('toggles sort direction', () => {
    const onSortChange = jest.fn();
    const { getByText, getByTestId } = render(
      <SearchBar onSortChange={onSortChange} />
    );
    
    fireEvent.click(getByText('Sort by'));
    fireEvent.click(getByText('Date'));
    fireEvent.click(getByTestId('sort-direction'));
    
    expect(onSortChange).toHaveBeenCalledWith({
      field: 'date',
      direction: 'asc'
    });
  });
});
```

### 4. Advanced Search Tests
```typescript
describe('SearchBar Advanced Search', () => {
  it('handles advanced search syntax', () => {
    const onSearch = jest.fn();
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={onSearch} />
    );
    
    const input = getByPlaceholderText('Search chats...');
    fireEvent.change(input, {
      target: { value: 'platform:chatgpt date:>2024-03-01' }
    });
    
    expect(onSearch).toHaveBeenCalledWith({
      query: '',
      filters: {
        platform: 'chatgpt',
        date: { gt: '2024-03-01' }
      }
    });
  });

  it('validates advanced search syntax', () => {
    const { getByPlaceholderText, getByText } = render(<SearchBar />);
    
    const input = getByPlaceholderText('Search chats...');
    fireEvent.change(input, {
      target: { value: 'platform:invalid date:not-a-date' }
    });
    
    expect(getByText('Invalid search syntax')).toBeInTheDocument();
  });

  it('supports multiple filters in advanced search', () => {
    const onSearch = jest.fn();
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={onSearch} />
    );
    
    const input = getByPlaceholderText('Search chats...');
    fireEvent.change(input, {
      target: {
        value: 'test platform:chatgpt status:processed date:>2024-03-01'
      }
    });
    
    expect(onSearch).toHaveBeenCalledWith({
      query: 'test',
      filters: {
        platform: 'chatgpt',
        status: 'processed',
        date: { gt: '2024-03-01' }
      }
    });
  });
});
```

### 5. Integration Tests
```typescript
describe('SearchBar Integration', () => {
  it('combines search, filters, and sort', () => {
    const onSearch = jest.fn();
    const { getByPlaceholderText, getByText } = render(
      <SearchBar onSearch={onSearch} />
    );
    
    // Enter search query
    const input = getByPlaceholderText('Search chats...');
    fireEvent.change(input, {
      target: { value: 'test' }
    });
    
    // Apply filters
    fireEvent.click(getByText('Platform'));
    fireEvent.click(getByText('ChatGPT'));
    
    fireEvent.click(getByText('Date'));
    fireEvent.change(getByLabelText('Start date'), {
      target: { value: '2024-03-01' }
    });
    
    // Apply sort
    fireEvent.click(getByText('Sort by'));
    fireEvent.click(getByText('Date'));
    
    expect(onSearch).toHaveBeenCalledWith({
      query: 'test',
      filters: {
        platform: 'chatgpt',
        dateRange: {
          start: '2024-03-01'
        }
      },
      sort: {
        field: 'date',
        direction: 'desc'
      }
    });
  });

  it('persists search state', () => {
    const { getByPlaceholderText, getByText, rerender } = render(
      <SearchBar initialState={{
        query: 'test',
        filters: {
          platform: 'chatgpt'
        },
        sort: {
          field: 'date',
          direction: 'desc'
        }
      }} />
    );
    
    expect(getByPlaceholderText('Search chats...').value).toBe('test');
    expect(getByText('ChatGPT')).toHaveClass('selected');
    expect(getByText('Date')).toHaveClass('active');
  });
});
```

## Test Coverage
- Basic search functionality
- Filter options
- Sort functionality
- Advanced search syntax
- State persistence

## Recent Updates
- Added advanced search tests
- Enhanced filter validation
- Improved integration tests
- Added state persistence tests
- Updated mocks
