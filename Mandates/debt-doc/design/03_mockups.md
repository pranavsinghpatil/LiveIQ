# ChatSynth UI Mockups

## Main Dashboard

### Header Component
```tsx
const Header: React.FC = () => (
  <header className="flex items-center justify-between h-16 px-6 bg-white border-b">
    <div className="flex items-center space-x-4">
      <Logo />
      <SearchBar />
    </div>
    <div className="flex items-center space-x-4">
      <NotificationBell />
      <UserProfile />
    </div>
  </header>
);
```

### Sidebar Navigation
```tsx
const Sidebar: React.FC = () => (
  <aside className="w-64 h-screen bg-white border-r">
    <div className="p-4">
      <button className="w-full btn-primary">
        + New Chat
      </button>
    </div>
    
    <nav className="space-y-6 p-4">
      {/* Recent Chats */}
      <section>
        <h3 className="text-sm font-semibold text-neutral-600">
          Recent Chats
        </h3>
        <ul className="mt-2 space-y-1">
          {recentChats.map(chat => (
            <ChatListItem key={chat.id} chat={chat} />
          ))}
        </ul>
      </section>
      
      {/* Tags */}
      <section>
        <h3 className="text-sm font-semibold text-neutral-600">
          Tags
        </h3>
        <ul className="mt-2 space-y-1">
          {tags.map(tag => (
            <TagListItem key={tag.id} tag={tag} />
          ))}
        </ul>
      </section>
      
      {/* Sources */}
      <section>
        <h3 className="text-sm font-semibold text-neutral-600">
          Sources
        </h3>
        <ul className="mt-2 space-y-1">
          <SourceItem source="chatgpt" />
          <SourceItem source="mistral" />
          <SourceItem source="gemini" />
        </ul>
      </section>
    </nav>
  </aside>
);
```

### Chat Interface
```tsx
const ChatView: React.FC<{ chatId: string }> = ({ chatId }) => (
  <div className="flex flex-col h-screen">
    {/* Chat Header */}
    <header className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center space-x-4">
        <h2 className="text-xl font-semibold">
          {chat.title}
        </h2>
        <span className={`badge badge-${chat.source}`}>
          {chat.source}
        </span>
      </div>
      <div className="flex items-center space-x-2">
        <button className="btn-outline">
          <ShareIcon />
        </button>
        <button className="btn-outline">
          <MoreIcon />
        </button>
      </div>
    </header>
    
    {/* Messages */}
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {chat.messages.map(message => (
        <ChatMessage
          key={message.id}
          message={message}
          onEdit={handleEdit}
        />
      ))}
    </div>
    
    {/* Input Area */}
    <div className="p-4 border-t bg-white">
      <form onSubmit={handleSend} className="flex space-x-2">
        <input
          type="text"
          className="flex-1 input"
          placeholder="Type your message..."
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <button type="submit" className="btn-primary">
          Send
        </button>
      </form>
    </div>
  </div>
);
```

### Message Component
```tsx
const ChatMessage: React.FC<{
  message: Message;
  onEdit?: (id: string, content: string) => void;
}> = ({ message, onEdit }) => (
  <div className={`chat-message ${message.role}`}>
    <div className="flex items-start space-x-3">
      <div className="flex-shrink-0">
        {message.role === 'user' ? (
          <UserAvatar />
        ) : (
          <AssistantAvatar source={message.source} />
        )}
      </div>
      
      <div className="flex-1 space-y-1">
        <div className="flex items-center space-x-2">
          <span className="font-medium">
            {message.role === 'user' ? 'You' : 'Assistant'}
          </span>
          <span className="text-sm text-neutral-500">
            {formatTime(message.timestamp)}
          </span>
        </div>
        
        <div className="prose max-w-none">
          {message.content}
        </div>
        
        <div className="flex items-center space-x-2 mt-2">
          <button className="text-sm text-neutral-500 hover:text-neutral-700">
            Copy
          </button>
          {message.role === 'user' && onEdit && (
            <button
              className="text-sm text-neutral-500 hover:text-neutral-700"
              onClick={() => onEdit(message.id, message.content)}
            >
              Edit
            </button>
          )}
        </div>
      </div>
    </div>
  </div>
);
```

### Import Dialog
```tsx
const ImportDialog: React.FC<{
  isOpen: boolean;
  onClose: () => void;
}> = ({ isOpen, onClose }) => (
  <Dialog
    open={isOpen}
    onClose={onClose}
    className="relative z-50"
  >
    <div className="fixed inset-0 bg-black/30" />
    
    <div className="fixed inset-0 flex items-center justify-center">
      <Dialog.Panel className="w-full max-w-md bg-white rounded-lg shadow-xl">
        <div className="p-6">
          <Dialog.Title className="text-lg font-semibold">
            Import Chat
          </Dialog.Title>
          
          <form onSubmit={handleImport} className="mt-4 space-y-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium">
                Source
              </label>
              <select
                className="w-full input"
                value={source}
                onChange={e => setSource(e.target.value)}
              >
                <option value="">Auto-detect</option>
                <option value="chatgpt">ChatGPT</option>
                <option value="mistral">Mistral</option>
                <option value="gemini">Gemini</option>
              </select>
            </div>
            
            <div className="space-y-2">
              <label className="block text-sm font-medium">
                Content
              </label>
              <textarea
                className="w-full input min-h-[200px]"
                placeholder="Paste chat content here..."
                value={content}
                onChange={e => setContent(e.target.value)}
              />
            </div>
            
            <div className="flex justify-end space-x-2">
              <button
                type="button"
                className="btn-outline"
                onClick={onClose}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn-primary"
                disabled={!content}
              >
                Import
              </button>
            </div>
          </form>
        </div>
      </Dialog.Panel>
    </div>
  </Dialog>
);
```

### Search Interface
```tsx
const SearchView: React.FC = () => (
  <div className="p-6 space-y-6">
    {/* Search Header */}
    <div className="flex items-center space-x-4">
      <h1 className="text-2xl font-semibold">Search</h1>
      <div className="flex-1">
        <input
          type="text"
          className="w-full input"
          placeholder="Search chats..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
      </div>
    </div>
    
    {/* Filters */}
    <div className="flex items-center space-x-4">
      <DateRangePicker
        startDate={startDate}
        endDate={endDate}
        onChange={handleDateChange}
      />
      
      <Select
        value={source}
        onChange={setSource}
        options={sourceOptions}
        placeholder="All Sources"
      />
      
      <TagSelect
        value={selectedTags}
        onChange={setSelectedTags}
        options={availableTags}
      />
    </div>
    
    {/* Results */}
    <div className="space-y-4">
      {results.map(result => (
        <SearchResult
          key={result.id}
          result={result}
          query={query}
        />
      ))}
    </div>
  </div>
);
```

### Mobile Layout
```tsx
const MobileLayout: React.FC = () => (
  <div className="h-screen flex flex-col">
    {/* Mobile Header */}
    <header className="flex items-center justify-between p-4 border-b">
      <button onClick={toggleSidebar}>
        <MenuIcon />
      </button>
      <Logo />
      <button onClick={toggleProfile}>
        <UserIcon />
      </button>
    </header>
    
    {/* Main Content */}
    <main className="flex-1 overflow-y-auto">
      {children}
    </main>
    
    {/* Bottom Navigation */}
    <nav className="flex items-center justify-around p-4 border-t bg-white">
      <NavButton icon={HomeIcon} label="Home" />
      <NavButton icon={SearchIcon} label="Search" />
      <NavButton icon={TagIcon} label="Tags" />
      <NavButton icon={MoreIcon} label="More" />
    </nav>
    
    {/* Slide-out Sidebar */}
    <Transition show={sidebarOpen}>
      <div className="fixed inset-0 z-50">
        <div className="absolute inset-0 bg-black/30" />
        <div className="absolute inset-y-0 left-0 w-64 bg-white">
          <Sidebar />
        </div>
      </div>
    </Transition>
  </div>
);
```

## Component Library

Our component library is built with:
- TailwindCSS for styling
- HeadlessUI for accessible components
- React Icons for iconography
- React Spring for animations

### Base Components
1. Buttons (Primary, Secondary, Outline)
2. Input fields
3. Select dropdowns
4. Tags
5. Cards
6. Modals
7. Toast notifications

### Custom Components
1. Chat message bubbles
2. Source badges
3. Tag pills
4. Search filters
5. Navigation items
6. Loading states

## Responsive Design

### Breakpoints
```css
/* Mobile First */
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Tablet (640px) */
@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

/* Laptop (1024px) */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

/* Desktop (1280px) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}
```

### Layout Changes
1. Mobile:
   - Bottom navigation
   - Full-screen modals
   - Stacked filters
   - Compact message view

2. Tablet:
   - Side navigation (collapsible)
   - Slide-in modals
   - Horizontal filters
   - Regular message view

3. Desktop:
   - Persistent sidebar
   - Center-screen modals
   - Advanced filters
   - Expanded message view

## Animations

### Transitions
```tsx
// Page Transitions
const pageVariants = {
  initial: { opacity: 0, x: -20 },
  enter: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 }
};

// Modal Transitions
const modalVariants = {
  initial: { opacity: 0, scale: 0.95 },
  enter: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 }
};

// Sidebar Transitions
const sidebarVariants = {
  open: { x: 0 },
  closed: { x: "-100%" }
};
```

### Loading States
```tsx
const LoadingSpinner: React.FC = () => (
  <div className="animate-spin rounded-full h-5 w-5 border-2 border-primary-500 border-t-transparent" />
);

const LoadingDots: React.FC = () => (
  <div className="space-x-1">
    <span className="animate-bounce">•</span>
    <span className="animate-bounce delay-100">•</span>
    <span className="animate-bounce delay-200">•</span>
  </div>
);
```

## Next Steps

1. Implement component library
2. Build responsive layouts
3. Add animations and transitions
4. Test across devices
5. Gather user feedback
