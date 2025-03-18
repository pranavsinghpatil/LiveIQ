# ChatSynth Wireframes

## Layout Structure

### Main Layout
```
+------------------+------------------+
|      Header      |     Profile     |
+--------+---------+------------------+
|        |                           |
| Sidebar|         Main Content      |
|        |                           |
|        |                           |
+--------+---------------------------+
```

### Header (Top Bar)
```
+-------+--------+----------------+---+
| Logo  | Search | Notifications | 👤 |
+-------+--------+----------------+---+
```

### Sidebar (Navigation)
```
+----------------------+
| + New Chat           |
+----------------------+
| Recent Chats         |
| ├─ Chat 1           |
| ├─ Chat 2           |
| └─ Chat 3           |
+----------------------+
| Tags                 |
| ├─ Work             |
| ├─ Personal         |
| └─ Learning         |
+----------------------+
| Sources             |
| ├─ ChatGPT         |
| ├─ Mistral         |
| └─ Gemini          |
+----------------------+
```

### Chat View
```
+--------------------------------+
| Chat Title                     |
+--------------------------------+
| Message 1 (User)               |
| ├─ Content                     |
| └─ Timestamp                   |
+--------------------------------+
| Message 2 (Assistant)          |
| ├─ Content                     |
| └─ Timestamp                   |
+--------------------------------+
| Message Input                  |
| [Type a message...]    [Send] |
+--------------------------------+
```

### Import Dialog
```
+--------------------------------+
| Import Chat                    |
+--------------------------------+
| Source:                        |
| [ChatGPT ▼]                   |
+--------------------------------+
| Content:                       |
| +----------------------------+ |
| |                            | |
| |     Paste chat here...     | |
| |                            | |
| +----------------------------+ |
+--------------------------------+
| [Cancel]            [Import]   |
+--------------------------------+
```

### Search Interface
```
+--------------------------------+
| Search Results                 |
+--------------------------------+
| Filters:                       |
| Date: [Start] - [End]         |
| Source: [All Sources ▼]       |
| Tags: [Select Tags...]        |
+--------------------------------+
| Results:                       |
| ┌──────────────────────────┐  |
| │ Chat 1                   │  |
| │ Matched content...       │  |
| └──────────────────────────┘  |
| ┌──────────────────────────┐  |
| │ Chat 2                   │  |
| │ Matched content...       │  |
| └──────────────────────────┘  |
+--------------------------------+
```

### Tag Management
```
+--------------------------------+
| Tags                          |
+--------------------------------+
| + New Tag                     |
+--------------------------------+
| ┌──────────────────────────┐  |
| │ Work                     │  |
| │ [Color] [Edit] [Delete]  │  |
| └──────────────────────────┘  |
| ┌──────────────────────────┐  |
| │ Personal                 │  |
| │ [Color] [Edit] [Delete]  │  |
| └──────────────────────────┘  |
+--------------------------------+
```

### Settings Panel
```
+--------------------------------+
| Settings                       |
+--------------------------------+
| Profile                        |
| ├─ Name: [John Doe]           |
| └─ Email: [john@example.com]  |
+--------------------------------+
| Appearance                     |
| └─ Theme: [Light ▼]           |
+--------------------------------+
| Notifications                  |
| └─ [✓] Enable notifications   |
+--------------------------------+
| Export                         |
| └─ [Export All Chats]         |
+--------------------------------+
```

## Mobile Layout

### Mobile Navigation
```
+--------------------------------+
| ☰ Logo              👤        |
+--------------------------------+
| [Search...]                    |
+--------------------------------+
| Content                        |
|                               |
|                               |
|                               |
+--------------------------------+
| [Home] [Search] [Tags] [More] |
+--------------------------------+
```

### Mobile Chat View
```
+--------------------------------+
| ← Chat Title                   |
+--------------------------------+
| Messages                       |
|                               |
|                               |
|                               |
|                               |
+--------------------------------+
| [Message...]         [Send]    |
+--------------------------------+
```

## Responsive Behavior

### Desktop (>1024px)
- Full sidebar visible
- Multi-column layout
- Expanded search filters
- Detailed chat previews

### Tablet (768px - 1024px)
- Collapsible sidebar
- Single column layout
- Compact search filters
- Simplified chat previews

### Mobile (<768px)
- Bottom navigation
- Full-screen modals
- Stacked filters
- Minimal chat previews

## Interactive Elements

### Buttons
```
[ Primary Button ]  
[ Secondary Button ]
[ Ghost Button ]
```

### Input Fields
```
┌─────────────────────┐
│ Input Field         │
└─────────────────────┘

┌─────────────────────┐
│ Search...     🔍    │
└─────────────────────┘
```

### Dropdowns
```
┌─────────────────────┐
│ Selected Option  ▼  │
└─────────────────────┘
```

### Tags
```
┌──────┐ ┌──────┐ ┌──────┐
│ Tag1 │ │ Tag2 │ │ Tag3 │
└──────┘ └──────┘ └──────┘
```

### Loading States
```
[ Loading... ]
[ • • • ]
[ ━━━━━━━━━ ]
```

### Tooltips
```
┌─────────────┐
│  Tooltip    │
└─────────────┘
      │
   [Element]
```

## Next Steps

1. Create high-fidelity mockups based on these wireframes
2. Add interactions and animations
3. Implement responsive behavior
4. Build component library
