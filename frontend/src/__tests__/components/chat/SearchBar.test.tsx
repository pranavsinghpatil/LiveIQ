import { render, screen, fireEvent } from '@testing-library/react';
import { SearchBar } from '../../../components/chat/SearchBar';

describe('SearchBar', () => {
  const mockOnSearch = jest.fn();
  const mockOnPlatformChange = jest.fn();
  const defaultProps = {
    searchTerm: '',
    onSearch: mockOnSearch,
    onPlatformChange: mockOnPlatformChange,
    selectedPlatform: null,
    platforms: [
      { id: 'chatgpt', name: 'ChatGPT' },
      { id: 'gemini', name: 'Gemini' },
      { id: 'mistral', name: 'Mistral' }
    ]
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders search input and platform select', () => {
    render(<SearchBar {...defaultProps} />);
    
    expect(screen.getByPlaceholderText('Search chats...')).toBeInTheDocument();
    expect(screen.getByRole('combobox')).toBeInTheDocument();
  });

  it('calls onSearch when input value changes', () => {
    render(<SearchBar {...defaultProps} />);
    
    const input = screen.getByPlaceholderText('Search chats...');
    fireEvent.change(input, { target: { value: 'test search' } });
    
    expect(mockOnSearch).toHaveBeenCalledWith('test search');
  });

  it('calls onPlatformChange when platform is selected', () => {
    render(<SearchBar {...defaultProps} />);
    
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'chatgpt' } });
    
    expect(mockOnPlatformChange).toHaveBeenCalledWith('chatgpt');
  });

  it('displays selected platform', () => {
    render(
      <SearchBar
        {...defaultProps}
        selectedPlatform="chatgpt"
      />
    );
    
    const select = screen.getByRole('combobox') as HTMLSelectElement;
    expect(select.value).toBe('chatgpt');
  });

  it('shows all platforms in dropdown', () => {
    render(<SearchBar {...defaultProps} />);
    
    const options = screen.getAllByRole('option');
    expect(options).toHaveLength(4); // Including "All Platforms" option
    expect(options[0]).toHaveValue('');
    expect(options[1]).toHaveValue('chatgpt');
    expect(options[2]).toHaveValue('gemini');
    expect(options[3]).toHaveValue('mistral');
  });
});
