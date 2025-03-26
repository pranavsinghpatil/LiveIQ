# ImportChat Component

## Purpose
The ImportChat component is a critical part of VoxStitch (formerly ChatSynth) that enables users to import conversations from various AI platforms. It supports multiple import methods including URLs, file uploads, and media content (video/audio) with optional transcripts.

## Properties (Props)

| Prop Name | Type | Default | Description |
|-----------|------|---------|-------------|
| `isOpen` | boolean | `false` | Controls whether the import dialog is visible |
| `onClose` | function | `() => {}` | Callback function when dialog is closed |
| `standalone` | boolean | `false` | When true, the component manages its own visibility without parent control |
| `onImportSuccess` | function | `undefined` | Callback function when import is successful, receives the response data |

## State Management

The component manages several internal states:
- `localIsOpen`: Controls dialog visibility when in standalone mode
- `importType`: The selected import method ('link', 'file', 'video', 'audio')
- `platform`: The selected AI platform or source
- `customPlatform`: User-provided platform name when 'other' is selected
- `linkUrl`: URL input for link imports
- `file`: The selected file for upload
- `transcript`: Optional transcript file for video/audio imports
- `error`: Error message state
- `isLoading`: Loading state during import operation

## User Limits Integration

The component integrates with the authentication system to enforce guest user limits:
- Guest users have a limit of 2 chat imports
- The `hasReachedImportLimit()` function checks against the auth store's user data
- When limits are reached, appropriate messaging guides users to sign up

## UI Design

The component features a modern gradient-based design with:
- Gradient backgrounds instead of solid colors
- Smooth transitions and animations
- Platform-specific input fields that change based on the selected import type
- Responsive layout with proper spacing and alignment
- Accessibility features including proper focus states

## API Integration

The component sends import requests to the backend `/chats/import` endpoint using:
- FormData for proper file uploads
- Content-Type headers for multipart/form-data
- Error handling for different API response scenarios
- Loading states during API calls

## Accessibility and UX

- All inputs have descriptive labels
- Error states are clearly communicated with visual cues
- Focus management between inputs
- Proper button states (disabled during loading)
- Keyboard navigation support

## Relation to Other Components

The ImportChat component is typically used in:
1. The Sidebar for quick access to import functionality
2. Dedicated import pages where it can run in standalone mode
3. It communicates with the auth store to check user permissions and limits

## Recent Improvements

- Fixed dialog open prop issue for proper rendering
- Replaced solid colors with gradient designs
- Added proper error handling for API responses
- Improved typing for better TypeScript integration
- Enhanced user feedback during operations
