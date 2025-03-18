# Extended Features Design

## 1. Universal Chat Import System

### Import Sources
```tsx
// Extended source options
interface ImportSource {
  type: 'ai' | 'social' | 'podcast' | 'file' | 'cloud' | 'media';
  platform: string;
  icon: React.ReactNode;
  supportedFormats: string[];
}

const importSources: ImportSource[] = [
  // AI Platforms
  { 
    type: 'ai', 
    platform: 'chatgpt', 
    icon: <ChatGPTIcon />,
    supportedFormats: ['text', 'json', 'html']
  },
  { 
    type: 'ai', 
    platform: 'claude', 
    icon: <ClaudeIcon />,
    supportedFormats: ['text', 'json', 'markdown'] 
  },
  { 
    type: 'ai', 
    platform: 'gemini', 
    icon: <GeminiIcon />,
    supportedFormats: ['text', 'json', 'markdown'] 
  },
  { 
    type: 'ai', 
    platform: 'custom', 
    icon: <AIIcon />,
    supportedFormats: ['*'] 
  },
  
  // Social Media
  { 
    type: 'social', 
    platform: 'twitter', 
    icon: <TwitterIcon />,
    supportedFormats: ['text', 'json', 'html'] 
  },
  { 
    type: 'social', 
    platform: 'discord', 
    icon: <DiscordIcon />,
    supportedFormats: ['text', 'json'] 
  },
  { 
    type: 'social', 
    platform: 'slack', 
    icon: <SlackIcon />,
    supportedFormats: ['text', 'json', 'html'] 
  },
  
  // Cloud Storage
  { 
    type: 'cloud', 
    platform: 'googledrive', 
    icon: <GDriveIcon />,
    supportedFormats: ['*'] 
  },
  { 
    type: 'cloud', 
    platform: 'dropbox', 
    icon: <DropboxIcon />,
    supportedFormats: ['*'] 
  },
  { 
    type: 'cloud', 
    platform: 'onedrive', 
    icon: <OneDriveIcon />,
    supportedFormats: ['*'] 
  },
  
  // Media Types
  { 
    type: 'podcast', 
    platform: 'youtube', 
    icon: <YoutubeIcon />,
    supportedFormats: ['video', 'audio', 'transcript'] 
  },
  { 
    type: 'podcast', 
    platform: 'spotify', 
    icon: <SpotifyIcon />,
    supportedFormats: ['audio', 'transcript'] 
  },
  { 
    type: 'media', 
    platform: 'images/screenshots', 
    icon: <ImagesIcon />,
    supportedFormats: ['png', 'jpg', 'gif', 'webp'] 
  },
  { 
    type: 'media', 
    platform: 'video', 
    icon: <VideoIcon />,
    supportedFormats: ['mp4', 'webm', 'mov'] 
  }
];

### Enhanced Import Dialog
```tsx
const EnhancedImportDialog: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'paste' | 'file' | 'cloud'>('paste');
  const [selectedSource, setSelectedSource] = useState<ImportSource | null>(null);
  const [selectedFormat, setSelectedFormat] = useState<string>('');
  
  return (
    <Dialog className="max-w-2xl">
      <Tabs value={activeTab} onChange={setActiveTab}>
        <TabList>
          <Tab value="paste">Paste Content</Tab>
          <Tab value="file">Local File</Tab>
          <Tab value="cloud">Cloud Storage</Tab>
        </TabList>
        
        <TabPanel value="paste">
          <div className="space-y-4">
            <SourceSelector
              sources={importSources}
              value={selectedSource}
              onChange={setSelectedSource}
            />
            
            {selectedSource && (
              <FormatSelector
                formats={selectedSource.supportedFormats}
                value={selectedFormat}
                onChange={setSelectedFormat}
              />
            )}
            
            <textarea
              className="w-full h-64 input"
              placeholder={`Paste your ${selectedSource?.platform || ''} content here...`}
            />
          </div>
        </TabPanel>
        
        <TabPanel value="file">
          <FileUploader
            accept={selectedSource?.supportedFormats.map(f => `.${f}`).join(',')}
            onUpload={handleFileUpload}
            source={selectedSource}
          />
        </TabPanel>
        
        <TabPanel value="cloud">
          <CloudStorageConnector
            services={['googledrive', 'dropbox', 'onedrive']}
            onSelect={handleCloudFileSelect}
            source={selectedSource}
          />
        </TabPanel>
      </Tabs>
      
      <div className="p-4 border-t">
        <div className="flex justify-between">
          <button className="btn-outline" onClick={onCancel}>
            Cancel
          </button>
          <button 
            className="btn-primary"
            disabled={!selectedSource || !selectedFormat}
            onClick={handleImport}
          >
            Import Content
          </button>
        </div>
      </div>
    </Dialog>
  );
};
```

## 2. Chat Merger System

### Merger Interface
```tsx
const ChatMerger: React.FC = () => {
  const [selectedChats, setSelectedChats] = useState<Chat[]>([]);
  const [mergeStrategy, setMergeStrategy] = useState<'auto' | 'manual'>('auto');
  
  return (
    <div className="space-y-6">
      <header>
        <h2>Merge Conversations</h2>
        <p>Combine multiple chats into a unified conversation</p>
      </header>
      
      <div className="flex space-x-4">
        <div className="w-1/2">
          <h3>Selected Chats</h3>
          <ChatList
            chats={selectedChats}
            onSelect={handleChatSelect}
            onReorder={handleReorder}
          />
        </div>
        
        <div className="w-1/2">
          <h3>Merge Settings</h3>
          <div className="space-y-4">
            <RadioGroup
              value={mergeStrategy}
              onChange={setMergeStrategy}
            >
              <RadioOption value="auto">
                Auto-merge (AI-assisted)
              </RadioOption>
              <RadioOption value="manual">
                Manual arrangement
              </RadioOption>
            </RadioGroup>
            
            {mergeStrategy === 'manual' && (
              <ManualMergeControls
                chats={selectedChats}
                onUpdate={handleManualUpdate}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
```

### Hybrid Chat View
```tsx
const HybridChatView: React.FC = () => {
  const [focusMode, setFocusMode] = useState<'all' | string>('all');
  
  return (
    <div className="flex h-full">
      <div className="w-64 border-r">
        <SourceList
          sources={mergedSources}
          activeFocus={focusMode}
          onFocusChange={setFocusMode}
        />
      </div>
      
      <div className="flex-1">
        <ChatTimeline
          messages={messages}
          focusedSource={focusMode}
          onEdit={handleEdit}
          onMerge={handleMerge}
        />
      </div>
    </div>
  );
};
```

## 3. Conversation Analysis

### Analysis Dashboard
```tsx
const AnalysisDashboard: React.FC = () => {
  const [topics, setTopics] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  
  return (
    <div className="grid grid-cols-2 gap-6">
      <Card>
        <h3>Key Topics</h3>
        <TopicCloud topics={topics} />
      </Card>
      
      <Card>
        <h3>Conversation Starters</h3>
        <SuggestionList
          suggestions={suggestions}
          onSelect={handleSuggestionSelect}
        />
      </Card>
      
      <Card className="col-span-2">
        <h3>Timeline Analysis</h3>
        <TimelineGraph data={analysisData} />
      </Card>
    </div>
  );
};
```

## 4. Multi-Platform Response System

### Platform Selector
```tsx
const PlatformSelector: React.FC = () => {
  const [selectedPlatform, setSelectedPlatform] = useState<string>('auto');
  const [apiKey, setApiKey] = useState<string>('');
  
  return (
    <div className="space-y-4">
      <Select
        label="Response Platform"
        value={selectedPlatform}
        onChange={setSelectedPlatform}
        options={[
          { value: 'auto', label: 'Auto-select' },
          { value: 'chatgpt', label: 'ChatGPT' },
          { value: 'mistral', label: 'Mistral' },
          { value: 'gemini', label: 'Gemini' },
          // Add more platforms
        ]}
      />
      
      {selectedPlatform !== 'auto' && (
        <div className="space-y-2">
          <label>API Key</label>
          <input
            type="password"
            className="input"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
            placeholder="Enter your API key"
          />
        </div>
      )}
    </div>
  );
};
```

### Response Interface
```tsx
const ResponseInterface: React.FC = () => {
  const [platform, setPlatform] = useState<string>('auto');
  const [streaming, setStreaming] = useState<boolean>(false);
  
  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-4">
        <PlatformSelector
          value={platform}
          onChange={setPlatform}
        />
        
        <Switch
          label="Stream Response"
          checked={streaming}
          onChange={setStreaming}
        />
      </div>
      
      <div className="relative">
        <textarea
          className="w-full h-32 input"
          placeholder="Ask your question..."
        />
        
        <div className="absolute right-2 bottom-2">
          <button className="btn-primary">
            Send to {platform}
          </button>
        </div>
      </div>
    </div>
  );
};
```

## Mobile Considerations

### Mobile Import Flow
```tsx
const MobileImport: React.FC = () => (
  <div className="h-screen flex flex-col">
    <StepIndicator
      steps={['Source', 'Content', 'Review']}
      currentStep={currentStep}
    />
    
    <div className="flex-1 p-4">
      {currentStep === 'Source' && (
        <SourceGrid sources={importSources} />
      )}
      
      {currentStep === 'Content' && (
        <ContentInput type={selectedSource.type} />
      )}
      
      {currentStep === 'Review' && (
        <ImportPreview data={importData} />
      )}
    </div>
    
    <div className="p-4 border-t">
      <NavigationButtons
        onBack={handleBack}
        onNext={handleNext}
      />
    </div>
  </div>
);
```

### Mobile Merger
```tsx
const MobileMerger: React.FC = () => (
  <div className="h-screen flex flex-col">
    <header className="p-4 border-b">
      <h2>Merge Chats</h2>
    </header>
    
    <div className="flex-1 overflow-y-auto">
      <DraggableList
        items={selectedChats}
        onReorder={handleReorder}
        renderItem={chat => (
          <ChatPreview chat={chat} />
        )}
      />
    </div>
    
    <div className="p-4 border-t">
      <button className="w-full btn-primary">
        Merge Selected
      </button>
    </div>
  </div>
);
```

## Next Steps

1. Implement universal import system
   - File format handlers
   - Cloud storage integrations
   - Media processors

2. Build chat merger
   - AI-assisted merging
   - Manual controls
   - Focus mode

3. Add analysis features
   - Topic extraction
   - Suggestion generation
   - Timeline visualization

4. Integrate multi-platform responses
   - API management
   - Response streaming
   - Platform switching
