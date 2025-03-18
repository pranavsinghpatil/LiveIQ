# Podcast Integration Design

## 1. Podcast Import System

### Podcast Source Interface
```typescript
interface PodcastSource {
  type: 'podcast';
  platform: 'youtube' | 'spotify' | 'apple' | 'custom';
  format: 'video' | 'audio' | 'transcript';
  metadata: {
    title: string;
    participants: string[];
    duration: number;
    timestamp?: number;
    chapters?: {
      title: string;
      startTime: number;
      endTime: number;
    }[];
  };
}

interface PodcastImport {
  source: PodcastSource;
  content: {
    type: 'video' | 'audio' | 'transcript';
    data: string;  // URL or content
    segments?: {
      speaker: string;
      text: string;
      startTime: number;
      endTime: number;
    }[];
  };
}
```

### Podcast Import Dialog
```tsx
const PodcastImportDialog: React.FC = () => {
  const [source, setSource] = useState<PodcastSource['platform']>('youtube');
  const [format, setFormat] = useState<PodcastSource['format']>('video');
  const [url, setUrl] = useState('');
  
  return (
    <Dialog className="max-w-3xl">
      <div className="space-y-6 p-6">
        <header>
          <h2 className="text-2xl font-semibold">Import Podcast</h2>
          <p className="text-neutral-600">
            Import podcasts from various platforms and convert them into interactive chats
          </p>
        </header>
        
        {/* Source Selection */}
        <div className="grid grid-cols-4 gap-4">
          <PlatformButton
            platform="youtube"
            icon={<YoutubeIcon />}
            selected={source === 'youtube'}
            onClick={() => setSource('youtube')}
          />
          <PlatformButton
            platform="spotify"
            icon={<SpotifyIcon />}
            selected={source === 'spotify'}
            onClick={() => setSource('spotify')}
          />
          <PlatformButton
            platform="apple"
            icon={<ApplePodcastIcon />}
            selected={source === 'apple'}
            onClick={() => setSource('apple')}
          />
          <PlatformButton
            platform="custom"
            icon={<CustomIcon />}
            selected={source === 'custom'}
            onClick={() => setSource('custom')}
          />
        </div>
        
        {/* Format Selection */}
        <div className="flex space-x-4">
          <FormatOption
            value="video"
            label="Video"
            icon={<VideoIcon />}
            selected={format === 'video'}
            onClick={() => setFormat('video')}
          />
          <FormatOption
            value="audio"
            label="Audio"
            icon={<AudioIcon />}
            selected={format === 'audio'}
            onClick={() => setFormat('audio')}
          />
          <FormatOption
            value="transcript"
            label="Transcript"
            icon={<TranscriptIcon />}
            selected={format === 'transcript'}
            onClick={() => setFormat('transcript')}
          />
        </div>
        
        {/* URL Input */}
        <div className="space-y-2">
          <label className="text-sm font-medium">
            Podcast URL
          </label>
          <input
            type="url"
            className="w-full input"
            placeholder="Enter podcast URL..."
            value={url}
            onChange={e => setUrl(e.target.value)}
          />
        </div>
        
        {/* Advanced Options */}
        <Disclosure>
          <Disclosure.Button className="text-sm text-primary-600">
            Advanced Options
          </Disclosure.Button>
          
          <Disclosure.Panel className="space-y-4 mt-4">
            <div>
              <label className="text-sm font-medium">
                Start Time
              </label>
              <input
                type="text"
                className="input"
                placeholder="HH:MM:SS"
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">
                End Time
              </label>
              <input
                type="text"
                className="input"
                placeholder="HH:MM:SS"
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">
                Speaker Detection
              </label>
              <Switch
                checked={speakerDetection}
                onChange={setSpeakerDetection}
              />
            </div>
          </Disclosure.Panel>
        </Disclosure>
      </div>
    </Dialog>
  );
};
```

## 2. Podcast Chat View

### Chat Interface for Podcasts
```tsx
const PodcastChatView: React.FC<{ podcastId: string }> = ({ podcastId }) => {
  const [playbackTime, setPlaybackTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  
  return (
    <div className="flex h-screen">
      {/* Media Player */}
      <div className="w-1/2 border-r">
        <div className="p-4">
          <h2 className="text-xl font-semibold">
            {podcast.title}
          </h2>
          <div className="mt-2 text-sm text-neutral-600">
            {podcast.participants.join(', ')}
          </div>
        </div>
        
        <div className="aspect-video bg-black">
          {format === 'video' ? (
            <VideoPlayer
              url={podcast.content.data}
              currentTime={playbackTime}
              onTimeUpdate={setPlaybackTime}
              playing={isPlaying}
            />
          ) : (
            <AudioPlayer
              url={podcast.content.data}
              currentTime={playbackTime}
              onTimeUpdate={setPlaybackTime}
              playing={isPlaying}
            />
          )}
        </div>
        
        <div className="p-4">
          <PlaybackControls
            isPlaying={isPlaying}
            onPlayPause={() => setIsPlaying(!isPlaying)}
            onSeek={handleSeek}
            duration={podcast.metadata.duration}
            currentTime={playbackTime}
          />
        </div>
      </div>
      
      {/* Chat Messages */}
      <div className="w-1/2 flex flex-col">
        <div className="flex-1 overflow-y-auto p-4">
          {podcast.content.segments?.map(segment => (
            <ChatMessage
              key={segment.startTime}
              speaker={segment.speaker}
              content={segment.text}
              timestamp={segment.startTime}
              isActive={playbackTime >= segment.startTime && 
                       playbackTime <= segment.endTime}
              onClick={() => handleSegmentClick(segment)}
            />
          ))}
        </div>
        
        {/* User Input */}
        <div className="border-t p-4">
          <div className="space-y-4">
            <Select
              label="Ask or Continue as:"
              options={[
                { value: 'question', label: 'Ask a Question' },
                { value: 'continue', label: 'Continue Discussion' },
                { value: 'merge', label: 'Merge with Other Chat' }
              ]}
              value={interactionType}
              onChange={setInteractionType}
            />
            
            {interactionType === 'question' && (
              <div>
                <label className="text-sm font-medium">
                  Ask the Podcast Participants
                </label>
                <textarea
                  className="w-full input mt-2"
                  placeholder="What would you like to ask?"
                  value={question}
                  onChange={e => setQuestion(e.target.value)}
                />
              </div>
            )}
            
            {interactionType === 'continue' && (
              <div>
                <label className="text-sm font-medium">
                  Continue the Discussion
                </label>
                <textarea
                  className="w-full input mt-2"
                  placeholder="Add to the conversation..."
                  value={continuation}
                  onChange={e => setContinuation(e.target.value)}
                />
              </div>
            )}
            
            {interactionType === 'merge' && (
              <ChatMergeSelector
                currentPodcast={podcastId}
                onSelect={handleMergeSelect}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
```

## 3. Podcast-Chat Integration

### Hybrid Chat System
```tsx
interface HybridChatConfig {
  sources: {
    id: string;
    type: 'chat' | 'podcast';
    platform: string;
    title: string;
    participants?: string[];
  }[];
  mergeStrategy: {
    type: 'chronological' | 'topic' | 'custom';
    options: {
      preserveContext: boolean;
      linkRelatedContent: boolean;
      allowCrossPlatformResponses: boolean;
    };
  };
}

const HybridChatSystem: React.FC = () => {
  const [config, setConfig] = useState<HybridChatConfig>({
    sources: [],
    mergeStrategy: {
      type: 'chronological',
      options: {
        preserveContext: true,
        linkRelatedContent: true,
        allowCrossPlatformResponses: true
      }
    }
  });
  
  return (
    <div className="space-y-6">
      {/* Source Management */}
      <section>
        <h3>Chat Sources</h3>
        <div className="grid grid-cols-3 gap-4">
          {config.sources.map(source => (
            <SourceCard
              key={source.id}
              source={source}
              onRemove={() => handleRemoveSource(source.id)}
            />
          ))}
          <AddSourceButton onClick={handleAddSource} />
        </div>
      </section>
      
      {/* Merge Strategy */}
      <section>
        <h3>Merge Strategy</h3>
        <div className="space-y-4">
          <Select
            label="Organization"
            value={config.mergeStrategy.type}
            onChange={handleStrategyChange}
            options={[
              { value: 'chronological', label: 'Time-based' },
              { value: 'topic', label: 'Topic-based' },
              { value: 'custom', label: 'Custom Order' }
            ]}
          />
          
          <div className="space-y-2">
            <Toggle
              label="Preserve Original Context"
              checked={config.mergeStrategy.options.preserveContext}
              onChange={handleToggleContext}
            />
            <Toggle
              label="Link Related Content"
              checked={config.mergeStrategy.options.linkRelatedContent}
              onChange={handleToggleLinks}
            />
            <Toggle
              label="Allow Cross-platform Responses"
              checked={config.mergeStrategy.options.allowCrossPlatformResponses}
              onChange={handleToggleResponses}
            />
          </div>
        </div>
      </section>
      
      {/* Preview & Controls */}
      <section>
        <div className="flex justify-between">
          <h3>Preview</h3>
          <button
            className="btn-primary"
            onClick={handleMerge}
          >
            Create Hybrid Chat
          </button>
        </div>
        
        <div className="mt-4 border rounded-lg">
          <HybridChatPreview
            config={config}
            onUpdate={handlePreviewUpdate}
          />
        </div>
      </section>
    </div>
  );
};
```

## 4. AI Response System

### Platform-Specific Responses
```tsx
interface ResponseConfig {
  platform: string;
  context: {
    podcastSegments?: {
      startTime: number;
      endTime: number;
      text: string;
    }[];
    chatMessages?: {
      role: string;
      content: string;
    }[];
    currentTopic?: string;
    participants?: string[];
  };
  style?: {
    matchSpeaker?: string;
    tone?: 'casual' | 'formal' | 'expert';
    format?: 'direct' | 'elaborate' | 'socratic';
  };
}

const AIResponseSystem: React.FC = () => {
  const [config, setConfig] = useState<ResponseConfig>({
    platform: 'auto',
    context: {},
    style: {
      tone: 'casual',
      format: 'direct'
    }
  });
  
  return (
    <div className="space-y-6">
      {/* Platform Selection */}
      <section>
        <h3>Response Platform</h3>
        <div className="grid grid-cols-4 gap-4">
          <PlatformCard
            platform="auto"
            label="Auto-select"
            icon={<AutoIcon />}
            selected={config.platform === 'auto'}
            onClick={() => handlePlatformSelect('auto')}
          />
          <PlatformCard
            platform="chatgpt"
            label="ChatGPT"
            icon={<ChatGPTIcon />}
            selected={config.platform === 'chatgpt'}
            onClick={() => handlePlatformSelect('chatgpt')}
          />
          <PlatformCard
            platform="claude"
            label="Claude"
            icon={<ClaudeIcon />}
            selected={config.platform === 'claude'}
            onClick={() => handlePlatformSelect('claude')}
          />
          <PlatformCard
            platform="gemini"
            label="Gemini"
            icon={<GeminiIcon />}
            selected={config.platform === 'gemini'}
            onClick={() => handlePlatformSelect('gemini')}
          />
        </div>
      </section>
      
      {/* Response Style */}
      <section>
        <h3>Response Style</h3>
        <div className="space-y-4">
          {config.context.participants && (
            <Select
              label="Respond as"
              value={config.style?.matchSpeaker}
              onChange={handleSpeakerSelect}
              options={[
                { value: '', label: 'AI Assistant' },
                ...config.context.participants.map(p => ({
                  value: p,
                  label: p
                }))
              ]}
            />
          )}
          
          <Select
            label="Tone"
            value={config.style?.tone}
            onChange={handleToneSelect}
            options={[
              { value: 'casual', label: 'Casual' },
              { value: 'formal', label: 'Formal' },
              { value: 'expert', label: 'Expert' }
            ]}
          />
          
          <Select
            label="Format"
            value={config.style?.format}
            onChange={handleFormatSelect}
            options={[
              { value: 'direct', label: 'Direct Answer' },
              { value: 'elaborate', label: 'Detailed Explanation' },
              { value: 'socratic', label: 'Socratic Method' }
            ]}
          />
        </div>
      </section>
      
      {/* API Configuration */}
      <section>
        <h3>API Settings</h3>
        <div className="space-y-4">
          <input
            type="password"
            className="input"
            placeholder="Enter API Key"
            value={apiKey}
            onChange={handleApiKeyChange}
          />
          
          <div className="space-y-2">
            <Toggle
              label="Save API Key"
              checked={saveKey}
              onChange={setSaveKey}
            />
            <Toggle
              label="Stream Response"
              checked={streamResponse}
              onChange={setStreamResponse}
            />
          </div>
        </div>
      </section>
    </div>
  );
};
```

## Mobile Considerations

### Mobile Podcast View
```tsx
const MobilePodcastView: React.FC = () => (
  <div className="h-screen flex flex-col">
    {/* Header */}
    <header className="p-4 border-b">
      <h2 className="text-lg font-semibold">
        {podcast.title}
      </h2>
    </header>
    
    {/* Media Player (Collapsible) */}
    <div className="relative">
      <div className="aspect-video bg-black">
        <MediaPlayer />
      </div>
      <button
        className="absolute bottom-2 right-2 bg-black/50 rounded-full p-2"
        onClick={togglePlayerSize}
      >
        <MinimizeIcon />
      </button>
    </div>
    
    {/* Chat Messages */}
    <div className="flex-1 overflow-y-auto">
      <ChatMessages />
    </div>
    
    {/* Input Area */}
    <div className="border-t p-4">
      <UserInput />
    </div>
  </div>
);
```

## Next Steps

1. Implement Podcast Features
   - Video/audio player integration
   - Transcript synchronization
   - Speaker detection
   - Time-based navigation

2. Enhance Chat Integration
   - Cross-platform merging
   - Context preservation
   - Topic linking
   - Smart suggestions

3. Develop AI Response System
   - Platform-specific handlers
   - Style matching
   - Context awareness
   - Response streaming
