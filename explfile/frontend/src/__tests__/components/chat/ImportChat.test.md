# ImportChat Component Tests

## Purpose
Test suite for the ImportChat component, which handles importing chat conversations from various sources including text files, audio, video, and screenshots.

## Test Structure

### 1. Import Dialog Tests
```typescript
describe('ImportChat Dialog', () => {
  it('renders import options correctly', () => {
    const { getByText } = render(<ImportChat />);
    
    expect(getByText('Import from Link')).toBeInTheDocument();
    expect(getByText('Upload File')).toBeInTheDocument();
    expect(getByText('Import from Audio')).toBeInTheDocument();
    expect(getByText('Import from Video')).toBeInTheDocument();
  });

  it('validates chat link format', async () => {
    const { getByPlaceholderText, getByText } = render(<ImportChat />);
    const input = getByPlaceholderText('Paste chat link');
    
    // Test invalid link
    fireEvent.change(input, {
      target: { value: 'invalid-link' }
    });
    fireEvent.click(getByText('Import'));
    
    expect(await getByText('Invalid chat link format')).toBeInTheDocument();
    
    // Test valid link
    fireEvent.change(input, {
      target: { value: 'https://chat.openai.com/123' }
    });
    fireEvent.click(getByText('Import'));
    
    expect(mockImportChat).toHaveBeenCalledWith('https://chat.openai.com/123');
  });
});
```

### 2. File Upload Tests
```typescript
describe('File Upload', () => {
  it('handles text file upload', async () => {
    const file = new File(['chat content'], 'chat.txt', {
      type: 'text/plain'
    });
    
    const { getByLabelText } = render(<ImportChat />);
    const input = getByLabelText('Upload chat file');
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);
    
    expect(mockProcessFile).toHaveBeenCalledWith(file);
  });

  it('handles audio file upload', async () => {
    const file = new File(['audio content'], 'chat.mp3', {
      type: 'audio/mpeg'
    });
    
    const { getByLabelText } = render(<ImportChat />);
    const input = getByLabelText('Upload audio file');
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);
    
    expect(mockProcessAudio).toHaveBeenCalledWith(file);
  });

  it('handles video file upload', async () => {
    const file = new File(['video content'], 'chat.mp4', {
      type: 'video/mp4'
    });
    
    const { getByLabelText } = render(<ImportChat />);
    const input = getByLabelText('Upload video file');
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);
    
    expect(mockProcessVideo).toHaveBeenCalledWith(file);
  });
});
```

### 3. Processing Tests
```typescript
describe('Chat Processing', () => {
  it('processes text chat correctly', async () => {
    const chatData = {
      platform: 'chatgpt',
      messages: [
        { role: 'user', content: 'Hello' },
        { role: 'assistant', content: 'Hi there!' }
      ]
    };
    
    const { getByText } = render(<ImportChat initialData={chatData} />);
    
    fireEvent.click(getByText('Process Chat'));
    
    expect(mockProcessChat).toHaveBeenCalledWith(chatData);
    expect(await getByText('Chat processed successfully')).toBeInTheDocument();
  });

  it('processes audio chat correctly', async () => {
    const audioData = {
      type: 'audio',
      duration: '5:00',
      transcript: 'Transcribed chat content'
    };
    
    const { getByText } = render(<ImportChat initialData={audioData} />);
    
    fireEvent.click(getByText('Process Audio'));
    
    expect(mockProcessAudioChat).toHaveBeenCalledWith(audioData);
    expect(await getByText('Audio processed successfully')).toBeInTheDocument();
  });

  it('processes video chat correctly', async () => {
    const videoData = {
      type: 'video',
      duration: '10:00',
      transcript: 'Transcribed chat content',
      frames: ['frame1.jpg', 'frame2.jpg']
    };
    
    const { getByText } = render(<ImportChat initialData={videoData} />);
    
    fireEvent.click(getByText('Process Video'));
    
    expect(mockProcessVideoChat).toHaveBeenCalledWith(videoData);
    expect(await getByText('Video processed successfully')).toBeInTheDocument();
  });
});
```

### 4. Error Handling Tests
```typescript
describe('Error Handling', () => {
  it('handles network errors', async () => {
    mockImportChat.mockRejectedValue(new Error('Network error'));
    
    const { getByText } = render(<ImportChat />);
    
    fireEvent.click(getByText('Import'));
    
    expect(await getByText('Failed to import chat')).toBeInTheDocument();
    expect(await getByText('Network error')).toBeInTheDocument();
  });

  it('handles invalid file types', async () => {
    const file = new File(['invalid'], 'invalid.xyz', {
      type: 'application/xyz'
    });
    
    const { getByLabelText, getByText } = render(<ImportChat />);
    const input = getByLabelText('Upload file');
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);
    
    expect(await getByText('Invalid file type')).toBeInTheDocument();
  });

  it('handles processing errors', async () => {
    mockProcessChat.mockRejectedValue(new Error('Processing failed'));
    
    const { getByText } = render(<ImportChat />);
    
    fireEvent.click(getByText('Process Chat'));
    
    expect(await getByText('Failed to process chat')).toBeInTheDocument();
    expect(await getByText('Processing failed')).toBeInTheDocument();
  });
});
```

### 5. Integration Tests
```typescript
describe('Integration', () => {
  it('completes full import flow', async () => {
    const { getByText, getByLabelText } = render(<ImportChat />);
    
    // Upload file
    const file = new File(['chat content'], 'chat.txt', {
      type: 'text/plain'
    });
    const input = getByLabelText('Upload file');
    Object.defineProperty(input, 'files', { value: [file] });
    fireEvent.change(input);
    
    // Process chat
    await waitFor(() => {
      expect(getByText('Process Chat')).toBeEnabled();
    });
    fireEvent.click(getByText('Process Chat'));
    
    // Verify success
    expect(await getByText('Chat imported successfully')).toBeInTheDocument();
    expect(mockNavigate).toHaveBeenCalledWith('/chats/123');
  });

  it('handles multi-file import', async () => {
    const { getByText, getByLabelText } = render(<ImportChat />);
    
    // Upload multiple files
    const files = [
      new File(['chat 1'], 'chat1.txt', { type: 'text/plain' }),
      new File(['chat 2'], 'chat2.txt', { type: 'text/plain' })
    ];
    const input = getByLabelText('Upload files');
    Object.defineProperty(input, 'files', { value: files });
    fireEvent.change(input);
    
    // Process chats
    await waitFor(() => {
      expect(getByText('Process All')).toBeEnabled();
    });
    fireEvent.click(getByText('Process All'));
    
    // Verify success
    expect(await getByText('2 chats imported successfully')).toBeInTheDocument();
  });
});
```

## Test Coverage
- Import dialog rendering
- File upload handling
- Chat processing
- Error scenarios
- Integration flows

## Recent Updates
- Added video import tests
- Enhanced error handling
- Improved integration tests
- Added batch processing tests
- Updated mocks
