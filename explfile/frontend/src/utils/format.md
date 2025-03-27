# Format Utilities Documentation

## Overview
The format utilities provide functions for formatting dates, times, file sizes, and other common data types used throughout the application.

## Implementation

### Date and Time Formatting
```typescript
import { format, formatDistance } from 'date-fns';

/**
 * Format a date string into a human-readable format
 */
export const formatDate = (date: string | Date): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return format(d, 'MMM d, yyyy');
};

/**
 * Format a date string into a time string
 */
export const formatTime = (date: string | Date): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return format(d, 'h:mm a');
};

/**
 * Format a date string into a relative time string
 */
export const formatRelativeTime = (date: string | Date): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return formatDistance(d, new Date(), { addSuffix: true });
};

/**
 * Format a timestamp into a chat message time format
 */
export const formatMessageTime = (timestamp: string): string => {
  const date = new Date(timestamp);
  const now = new Date();
  
  // If same day, show time
  if (date.toDateString() === now.toDateString()) {
    return format(date, 'h:mm a');
  }
  
  // If within last 7 days, show day name
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
  if (diffDays < 7) {
    return format(date, 'EEEE h:mm a');
  }
  
  // Otherwise show full date
  return format(date, 'MMM d, yyyy h:mm a');
};
```

### File Size Formatting
```typescript
/**
 * Format a number of bytes into a human-readable size string
 */
export const formatBytes = (bytes: number): string => {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(1)} ${units[unitIndex]}`;
};

/**
 * Format a duration in seconds into a human-readable time string
 */
export const formatDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
  
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};
```

### Number Formatting
```typescript
/**
 * Format a number with thousands separators
 */
export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat().format(num);
};

/**
 * Format a number as a percentage
 */
export const formatPercent = (num: number): string => {
  return `${(num * 100).toFixed(1)}%`;
};

/**
 * Format a number as currency
 */
export const formatCurrency = (
  amount: number,
  currency: string = 'USD'
): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency
  }).format(amount);
};
```

### String Formatting
```typescript
/**
 * Truncate a string to a maximum length with ellipsis
 */
export const truncateString = (
  str: string,
  maxLength: number = 50
): string => {
  if (str.length <= maxLength) {
    return str;
  }
  
  return `${str.slice(0, maxLength)}...`;
};

/**
 * Convert a string to title case
 */
export const toTitleCase = (str: string): string => {
  return str
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

/**
 * Convert a string to kebab case
 */
export const toKebabCase = (str: string): string => {
  return str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
};

/**
 * Convert a string to camel case
 */
export const toCamelCase = (str: string): string => {
  return str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase());
};
```

### URL Formatting
```typescript
/**
 * Format a URL by removing trailing slashes and normalizing
 */
export const formatUrl = (url: string): string => {
  return url.replace(/\/+$/, '').toLowerCase();
};

/**
 * Extract domain from URL
 */
export const extractDomain = (url: string): string => {
  try {
    const { hostname } = new URL(url);
    return hostname;
  } catch {
    return '';
  }
};

/**
 * Generate a slug from a string
 */
export const generateSlug = (str: string): string => {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
};
```

### Chat Formatting
```typescript
/**
 * Format chat platform name for display
 */
export const formatPlatform = (platform: string): string => {
  switch (platform.toLowerCase()) {
    case 'chatgpt':
      return 'ChatGPT';
    case 'mistral':
      return 'Mistral AI';
    case 'gemini':
      return 'Google Gemini';
    default:
      return toTitleCase(platform);
  }
};

/**
 * Format chat message for display
 */
export const formatMessage = (message: string): string => {
  // Remove excessive newlines
  return message
    .replace(/\n{3,}/g, '\n\n')
    .trim();
};

/**
 * Format chat summary for display
 */
export const formatSummary = (summary: string): string => {
  return truncateString(summary, 200);
};
```

## Usage Examples

### Date Formatting
```typescript
const timestamp = '2025-03-27T12:34:56Z';

console.log(formatDate(timestamp));
// Output: Mar 27, 2025

console.log(formatTime(timestamp));
// Output: 12:34 PM

console.log(formatRelativeTime(timestamp));
// Output: 2 hours ago

console.log(formatMessageTime(timestamp));
// Output: Today 12:34 PM
```

### File Size Formatting
```typescript
console.log(formatBytes(1234));
// Output: 1.2 KB

console.log(formatDuration(125));
// Output: 2:05
```

### Number Formatting
```typescript
console.log(formatNumber(1234567));
// Output: 1,234,567

console.log(formatPercent(0.1234));
// Output: 12.3%

console.log(formatCurrency(1234.56));
// Output: $1,234.56
```

### String Formatting
```typescript
console.log(truncateString('This is a very long string', 10));
// Output: This is...

console.log(toTitleCase('hello world'));
// Output: Hello World

console.log(toKebabCase('Hello World'));
// Output: hello-world

console.log(toCamelCase('hello-world'));
// Output: helloWorld
```

### URL Formatting
```typescript
console.log(formatUrl('https://example.com/'));
// Output: https://example.com

console.log(extractDomain('https://example.com/path'));
// Output: example.com

console.log(generateSlug('Hello World!'));
// Output: hello-world
```

### Chat Formatting
```typescript
console.log(formatPlatform('chatgpt'));
// Output: ChatGPT

console.log(formatMessage('Hello\n\n\nWorld'));
// Output: Hello\n\nWorld

console.log(formatSummary('A very long chat summary...'));
// Output: A very long chat... (truncated)
```
