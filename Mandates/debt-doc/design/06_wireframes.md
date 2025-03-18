# ChatSynth Wireframes

## 1. Main Layout

```
+------------------+--------------------------------+
|     Header       |                                |
+--------+---------+                                |
|        |         |                                |
|  Side  |  Main Content Area                      |
|  Nav   |                                         |
|        |                                         |
|        |                                         |
|        |                                         |
+--------+-----------------------------------------+

Header:
- Logo
- Search Bar
- User Profile
- Import Button
- Settings

Side Nav:
- Recent Chats
- Tags
- Sources
- Filters
```

## 2. Import Interface

```
+------------------------------------------+
|  Import Content                        X  |
+------------------------------------------+
|                                          |
|  [Paste] [File] [Cloud] [Link]          |
|                                          |
|  Source Selection:                       |
|  [AI] [Social] [Podcast] [Media]        |
|                                          |
|  Format Options:                         |
|  [Text] [Video] [Audio] [Transcript]    |
|                                          |
|  Content Area:                           |
|  +----------------------------------+    |
|  |                                  |    |
|  |                                  |    |
|  +----------------------------------+    |
|                                          |
|  Advanced Options:                       |
|  - Speaker Detection                     |
|  - Time Range                           |
|  - Format Settings                      |
|                                          |
|  [Cancel]                    [Import]    |
+------------------------------------------+
```

## 3. Chat Interface

```
+------------------------------------------+
|  Chat Title                    Actions   |
+------------------------------------------+
|                                          |
|  Message History                         |
|  +----------------------------------+    |
|  | User: Hello                      |    |
|  |                                  |    |
|  | Assistant: Hi there!             |    |
|  |                                  |    |
|  +----------------------------------+    |
|                                          |
|  Input Area:                            |
|  +----------------------------------+    |
|  | Type your message...             |    |
|  +----------------------------------+    |
|  [Platform Select]         [Send]        |
+------------------------------------------+
```

## 4. Podcast View

```
+------------------+------------------------+
|  Media Player    |  Chat/Transcript      |
|  +------------+  |  +----------------+   |
|  |            |  |  | Speaker 1:     |   |
|  |            |  |  | Hello everyone |   |
|  |            |  |  |                |   |
|  +------------+  |  | Speaker 2:     |   |
|                  |  | Hi there!      |   |
|  Controls:       |  |                |   |
|  [◀] [▶] [⏸]    |  +----------------+   |
|                  |                       |
|  Chapters:       |  Questions:          |
|  - Intro         |  [Ask Speaker 1]     |
|  - Topic 1       |  [Ask Speaker 2]     |
|  - Topic 2       |  [Continue Topic]    |
+------------------+-----------------------+
```

## 5. Hybrid Chat

```
+------------------------------------------+
|  Hybrid Chat Builder                   X  |
+------------------------------------------+
|                                          |
|  Source Selection:                       |
|  +----------------------------------+    |
|  | [✓] Chat 1                       |    |
|  | [✓] Podcast Segment              |    |
|  | [✓] Social Thread               |    |
|  +----------------------------------+    |
|                                          |
|  Merge Strategy:                         |
|  [Chronological] [Topic] [Custom]        |
|                                          |
|  Options:                                |
|  [✓] Preserve Context                    |
|  [✓] Link Related Content                |
|  [✓] Allow Cross-platform Responses      |
|                                          |
|  Preview:                                |
|  +----------------------------------+    |
|  |                                  |    |
|  |                                  |    |
|  +----------------------------------+    |
|                                          |
|  [Back]                    [Create]      |
+------------------------------------------+
```

## 6. Platform Response

```
+------------------------------------------+
|  Response Configuration               X  |
+------------------------------------------+
|                                          |
|  Platform:                               |
|  [Auto] [ChatGPT] [Claude] [Gemini]     |
|                                          |
|  Style:                                  |
|  - Respond as: [Select Speaker]          |
|  - Tone: [Casual/Formal/Expert]          |
|  - Format: [Direct/Detailed/Socratic]    |
|                                          |
|  API Settings:                           |
|  +----------------------------------+    |
|  | API Key: [****************]       |    |
|  +----------------------------------+    |
|  [✓] Save API Key                        |
|  [✓] Stream Response                     |
|                                          |
|  [Cancel]                    [Apply]      |
+------------------------------------------+
```

## 7. Mobile Layout

### A. Mobile Navigation
```
+------------------------------------------+
|  ☰  ChatSynth                  👤       |
+------------------------------------------+
|                                          |
|  Content Area                            |
|                                          |
|                                          |
|                                          |
|                                          |
+------------------------------------------+
|  [🏠] [🔍] [📝] [⚙️]                    |
+------------------------------------------+
```

### B. Mobile Podcast
```
+------------------------------------------+
|  ← Podcast Title              Share    |
+------------------------------------------+
|  +----------------------------------+    |
|  |           Video Player           |    |
|  |                                  |    |
|  +----------------------------------+    |
|  [Minimize]                             |
|                                          |
|  Chat/Transcript                         |
|  +----------------------------------+    |
|  |                                  |    |
|  |                                  |    |
|  +----------------------------------+    |
|                                          |
|  [Type your message...]                  |
+------------------------------------------+
```

## 8. Responsive Behavior

### Desktop (1280px+)
- Full sidebar
- Multi-column layout
- Advanced features visible

### Tablet (768px - 1279px)
- Collapsible sidebar
- Single-column layout with grid views
- Some features in dropdown menus

### Mobile (< 768px)
- Bottom navigation
- Stack layout
- Essential features only
- Swipe gestures
- Floating action buttons

## 9. States & Interactions

### Loading States
```
+------------------------------------------+
|  Loading...                              |
|  +----------------------------------+    |
|  |  ⚪⚪⚪                           |    |
|  |  Loading your content...         |    |
|  +----------------------------------+    |
+------------------------------------------+
```

### Error States
```
+------------------------------------------+
|  Error                               X   |
|  +----------------------------------+    |
|  |  ❌ Something went wrong          |    |
|  |  Please try again                |    |
|  +----------------------------------+    |
|  [Retry]                    [Cancel]     |
+------------------------------------------+
```

### Success States
```
+------------------------------------------+
|  Success                             X   |
|  +----------------------------------+    |
|  |  ✅ Content imported              |    |
|  |  Ready to start chatting         |    |
|  +----------------------------------+    |
|  [View Chat]                             |
+------------------------------------------+
```
