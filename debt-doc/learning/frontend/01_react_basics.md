# Understanding React in ChatSynth

## What is React?

React is a JavaScript library for building user interfaces. Think of it like building with Lego blocks - each piece (component) can be reused and combined to create something bigger.

## Basic Concepts

### 1. Components
Components are like building blocks. Each component is a piece of our interface:

```javascript
// Simple Component Example
// This is just a regular function that returns some HTML-like code
function WelcomeMessage() {
    return (
        <div className="welcome">
            <h1>Welcome to ChatSynth!</h1>
            <p>Your AI chat aggregator</p>
        </div>
    );
}

// Let's break this down:
// 1. function WelcomeMessage() - This creates our component
// 2. return (...) - What the component shows on screen
// 3. <div>, <h1>, <p> - These look like HTML but are actually JSX
```

### 2. Props (Properties)
Props are how we pass data to components:

```javascript
// Component that accepts props
function ChatMessage({ message, timestamp }) {
    // message and timestamp are props passed to this component
    
    return (
        <div className="chat-message">
            <p>{message}</p>
            <span className="timestamp">{timestamp}</span>
        </div>
    );
}

// Using the component
function ChatList() {
    return (
        <div>
            <ChatMessage 
                message="Hello there!"
                timestamp="2:30 PM"
            />
            <ChatMessage 
                message="Hi! How are you?"
                timestamp="2:31 PM"
            />
        </div>
    );
}

// Understanding props:
// 1. Props are like arguments to a function
// 2. They're passed like HTML attributes
// 3. We can access them inside the component
// 4. Props are read-only - never modify them!
```

### 3. State
State is data that can change over time:

```javascript
// Component with state
function Counter() {
    // useState creates a state variable
    const [count, setCount] = useState(0);
    // count: current value
    // setCount: function to change the value
    // 0: initial value
    
    return (
        <div>
            <p>You clicked {count} times</p>
            <button onClick={() => setCount(count + 1)}>
                Click me
            </button>
        </div>
    );
}

// Let's break down how state works:
// 1. useState(0) creates a state variable starting at 0
// 2. count holds the current value
// 3. setCount is used to change count
// 4. React automatically updates the screen when state changes
```

### 4. Real Example: Chat Input
Let's look at a real component from ChatSynth:

```javascript
// ChatInput.tsx - Where users type messages
function ChatInput({ onSendMessage }) {
    // State for the input text
    const [message, setMessage] = useState("");
    
    // Handle when user types
    const handleChange = (event) => {
        setMessage(event.target.value);
    };
    
    // Handle when user sends message
    const handleSubmit = (event) => {
        event.preventDefault();  // Prevent form submission
        
        if (message.trim()) {  // If message isn't empty
            onSendMessage(message);  // Send to parent
            setMessage("");  // Clear input
        }
    };
    
    return (
        <form onSubmit={handleSubmit} className="chat-input">
            <input
                type="text"
                value={message}
                onChange={handleChange}
                placeholder="Type your message..."
            />
            <button type="submit">Send</button>
        </form>
    );
}

// Let's understand each part:
// 1. State:
//    - message stores what user types
//    - setMessage updates the input value

// 2. Event Handlers:
//    - handleChange runs when user types
//    - handleSubmit runs when form is submitted

// 3. Props:
//    - onSendMessage is a function from parent component
//    - It's called when user sends a message

// 4. Form Elements:
//    - <input> is where user types
//    - <button> sends the message
```

### 5. Using Multiple Components
Components can be combined:

```javascript
// ChatWindow.tsx - Main chat interface
function ChatWindow() {
    // State for all messages
    const [messages, setMessages] = useState([]);
    
    // Add new message
    const handleNewMessage = (text) => {
        const newMessage = {
            id: Date.now(),  // Unique ID
            text: text,
            timestamp: new Date().toLocaleTimeString()
        };
        
        // Add to messages array
        setMessages([...messages, newMessage]);
    };
    
    return (
        <div className="chat-window">
            {/* Show all messages */}
            <div className="messages">
                {messages.map(msg => (
                    <ChatMessage
                        key={msg.id}
                        message={msg.text}
                        timestamp={msg.timestamp}
                    />
                ))}
            </div>
            
            {/* Input for new messages */}
            <ChatInput onSendMessage={handleNewMessage} />
        </div>
    );
}

// Understanding the structure:
// 1. ChatWindow contains:
//    - List of ChatMessage components
//    - One ChatInput component

// 2. Data flow:
//    - Messages stored in ChatWindow's state
//    - Passed to ChatMessage as props
//    - New messages come from ChatInput
```

### 6. Handling Side Effects
Sometimes we need to do things after the component renders:

```javascript
// ChatList.tsx - List of chat conversations
function ChatList() {
    // State for chats
    const [chats, setChats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // Load chats when component mounts
    useEffect(() => {
        // Async function to fetch chats
        async function loadChats() {
            try {
                setLoading(true);
                const response = await fetch('/api/chats');
                const data = await response.json();
                setChats(data);
            } catch (err) {
                setError('Failed to load chats');
            } finally {
                setLoading(false);
            }
        }
        
        loadChats();  // Run the function
    }, []);  // Empty array means run once when mounted
    
    // Show loading state
    if (loading) {
        return <div>Loading chats...</div>;
    }
    
    // Show error if any
    if (error) {
        return <div className="error">{error}</div>;
    }
    
    // Show chats
    return (
        <div className="chat-list">
            {chats.map(chat => (
                <ChatPreview
                    key={chat.id}
                    title={chat.title}
                    lastMessage={chat.lastMessage}
                    timestamp={chat.timestamp}
                />
            ))}
        </div>
    );
}

// Understanding useEffect:
// 1. useEffect runs after render
// 2. Perfect for data loading
// 3. Can clean up when component unmounts
// 4. Second argument ([]) controls when it runs
```

## Practice Exercise

Try to create a simple search component:
1. Input field for search term
2. State to store the term
3. Function to filter results
4. Display filtered results

Here's a starter template:
```javascript
function SearchChats({ chats }) {
    // Your code here
    return (
        <div>
            {/* Add search input */}
            {/* Show filtered chats */}
        </div>
    );
}
```

## Next Steps
1. Try the practice exercise
2. Learn about React hooks
3. Study component lifecycle
4. Explore state management (Redux)

## Common Questions

1. **When should I create a new component?**
   - When code is reused in multiple places
   - When a piece of UI has its own state
   - When a section is complex

2. **Props vs State?**
   - Props: Data passed from parent
   - State: Internal component data
   - Props are read-only
   - State can be changed

3. **Why use TypeScript?**
   - Catches errors early
   - Better code completion
   - Clearer code structure
   - Easier maintenance
