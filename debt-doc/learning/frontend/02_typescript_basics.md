# Understanding TypeScript in ChatSynth

## What is TypeScript?

TypeScript is like JavaScript with extra safety features. It helps us catch mistakes before they happen by adding types to our code. Think of it like having a spell checker for your code.

## Basic Types

### 1. Simple Types
Let's start with the basics:

```typescript
// Basic types
let name: string = "John";          // Text
let age: number = 25;               // Numbers
let isActive: boolean = true;       // True/False
let greeting: string;               // Declare without value

// Let's break these down:
// 1. : string tells TypeScript this must be text
// 2. : number means it must be a number
// 3. : boolean means true or false only
// 4. TypeScript will warn if we try to put wrong type
```

### 2. Arrays and Objects
How we work with lists and data:

```typescript
// Arrays (lists of things)
let messages: string[] = ["Hello", "World"];  // List of text
let numbers: number[] = [1, 2, 3];           // List of numbers

// Objects (groups of related data)
interface User {
    id: number;
    name: string;
    email: string;
    isAdmin?: boolean;  // ? means optional
}

// Using the interface
let user: User = {
    id: 1,
    name: "John",
    email: "john@example.com"
    // isAdmin is optional, so we can skip it
};

// Understanding these:
// 1. string[] means "list of strings"
// 2. interface defines shape of an object
// 3. ? makes properties optional
// 4. TypeScript checks if we're missing required properties
```

### 3. Real Example: Chat Message Types
Let's look at types we use in ChatSynth:

```typescript
// Types for chat messages
interface Message {
    id: number;
    content: string;
    role: "user" | "assistant";  // Only these two values allowed
    timestamp: string;
    metadata?: {
        platform: string;
        originalId: string;
    };
}

// Chat conversation type
interface ChatConversation {
    id: number;
    title: string;
    messages: Message[];
    source: "chatgpt" | "mistral" | "gemini";
    created_at: string;
    updated_at: string;
    tags: string[];
}

// Let's understand each part:
// 1. role: "user" | "assistant"
//    - Called a "union type"
//    - Can only be one of these values
//    - TypeScript will error for any other value

// 2. metadata?
//    - Optional property
//    - Might not exist on all messages

// 3. messages: Message[]
//    - Array of Message objects
//    - Must follow Message interface
```

### 4. Function Types
How we type our functions:

```typescript
// Function to send a message
interface SendMessageFunction {
    (content: string, chatId: number): Promise<Message>;
}

// Using the function type
const sendMessage: SendMessageFunction = async (content, chatId) => {
    const response = await fetch(`/api/chats/${chatId}/messages`, {
        method: 'POST',
        body: JSON.stringify({ content })
    });
    return response.json();
};

// Function with multiple parameters
interface ChatService {
    // Get chat by ID
    getChat(id: number): Promise<ChatConversation>;
    
    // Search chats with filters
    searchChats(query: string, filters?: {
        source?: string;
        dateRange?: {
            start: string;
            end: string;
        };
        tags?: string[];
    }): Promise<ChatConversation[]>;
}

// Understanding function types:
// 1. Parameters are typed: content: string
// 2. Return type after : Promise<Message>
// 3. TypeScript checks if we call with right types
// 4. Optional parameters marked with ?
```

### 5. React Component Types
How we type our React components:

```typescript
// Props interface for ChatMessage component
interface ChatMessageProps {
    message: Message;
    onEdit?: (id: number, newContent: string) => void;
    onDelete?: (id: number) => void;
    className?: string;
}

// Component with TypeScript
const ChatMessage: React.FC<ChatMessageProps> = ({
    message,
    onEdit,
    onDelete,
    className
}) => {
    return (
        <div className={`chat-message ${className || ''}`}>
            <p className={`role-${message.role}`}>
                {message.content}
            </p>
            <div className="actions">
                {onEdit && (
                    <button onClick={() => onEdit(message.id, message.content)}>
                        Edit
                    </button>
                )}
                {onDelete && (
                    <button onClick={() => onDelete(message.id)}>
                        Delete
                    </button>
                )}
            </div>
        </div>
    );
};

// Understanding component types:
// 1. React.FC means "Function Component"
// 2. <ChatMessageProps> defines what props it accepts
// 3. TypeScript checks if we pass correct props
// 4. Optional props can be left out
```

### 6. State and Hooks with Types
How to use TypeScript with React hooks:

```typescript
// Component with state and effects
const ChatList: React.FC = () => {
    // State with types
    const [chats, setChats] = useState<ChatConversation[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    // Effect to load chats
    useEffect(() => {
        const loadChats = async () => {
            try {
                const response = await fetch('/api/chats');
                const data: ChatConversation[] = await response.json();
                setChats(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load');
            } finally {
                setLoading(false);
            }
        };
        
        loadChats();
    }, []);
    
    // Custom hook with types
    const useDebounce = <T,>(value: T, delay: number): T => {
        const [debouncedValue, setDebouncedValue] = useState<T>(value);
        
        useEffect(() => {
            const timer = setTimeout(() => {
                setDebouncedValue(value);
            }, delay);
            
            return () => clearTimeout(timer);
        }, [value, delay]);
        
        return debouncedValue;
    };
    
    // Using the custom hook
    const [search, setSearch] = useState("");
    const debouncedSearch = useDebounce(search, 300);
    
    return (
        <div>
            {/* Component JSX */}
        </div>
    );
};

// Understanding typed hooks:
// 1. useState<Type> sets state type
// 2. Generic types like <T> for reusable code
// 3. Type inference where possible
// 4. Error handling with proper types
```

## Practice Exercise

Create a typed component for filtering chats:

```typescript
// Your task: Complete this component
interface FilterProps {
    onFilterChange: (filters: {
        source?: string;
        tags?: string[];
        dateRange?: {
            start: string;
            end: string;
        };
    }) => void;
    availableTags: string[];
    availableSources: string[];
}

const ChatFilter: React.FC<FilterProps> = () => {
    // Your code here
    return (
        <div>
            {/* Add filter controls */}
        </div>
    );
};
```

## Next Steps
1. Try the practice exercise
2. Learn about advanced types
3. Study type inference
4. Explore utility types

## Common Questions

1. **Why use TypeScript?**
   - Catches errors early
   - Better code completion
   - Self-documenting code
   - Easier to maintain

2. **When to use interfaces vs types?**
   - Interfaces for object shapes
   - Types for unions/intersections
   - Interfaces can be extended
   - Types can be computed

3. **Type inference?**
   - TypeScript can guess types
   - Less typing needed
   - Still safe
   - But explicit types help documentation
