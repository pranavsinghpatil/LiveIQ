# Validation Utilities Documentation

## Overview
The validation utilities provide functions for validating user input, form data, and file uploads throughout the application.

## Implementation

### Form Validation
```typescript
/**
 * Validate email format
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 */
export interface PasswordStrength {
  isValid: boolean;
  score: number;
  feedback: string[];
}

export const validatePassword = (password: string): PasswordStrength => {
  const result: PasswordStrength = {
    isValid: false,
    score: 0,
    feedback: []
  };
  
  // Length check
  if (password.length < 8) {
    result.feedback.push('Password must be at least 8 characters');
  } else {
    result.score += 20;
  }
  
  // Uppercase check
  if (!/[A-Z]/.test(password)) {
    result.feedback.push('Add uppercase letters');
  } else {
    result.score += 20;
  }
  
  // Lowercase check
  if (!/[a-z]/.test(password)) {
    result.feedback.push('Add lowercase letters');
  } else {
    result.score += 20;
  }
  
  // Number check
  if (!/\d/.test(password)) {
    result.feedback.push('Add numbers');
  } else {
    result.score += 20;
  }
  
  // Symbol check
  if (!/[!@#$%^&*]/.test(password)) {
    result.feedback.push('Add special characters');
  } else {
    result.score += 20;
  }
  
  result.isValid = result.score >= 80;
  return result;
};

/**
 * Validate form fields
 */
export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  validate?: (value: any) => boolean | string;
}

export interface ValidationError {
  field: string;
  message: string;
}

export const validateField = (
  value: any,
  rules: ValidationRule
): string | null => {
  if (rules.required && !value) {
    return 'This field is required';
  }
  
  if (typeof value === 'string') {
    if (rules.minLength && value.length < rules.minLength) {
      return `Minimum length is ${rules.minLength} characters`;
    }
    
    if (rules.maxLength && value.length > rules.maxLength) {
      return `Maximum length is ${rules.maxLength} characters`;
    }
    
    if (rules.pattern && !rules.pattern.test(value)) {
      return 'Invalid format';
    }
  }
  
  if (rules.validate) {
    const result = rules.validate(value);
    if (typeof result === 'string') {
      return result;
    }
    if (!result) {
      return 'Invalid value';
    }
  }
  
  return null;
};
```

### File Validation
```typescript
/**
 * Validate file type
 */
export interface FileTypeConfig {
  accept: string[];
  maxSize: number;
  minSize?: number;
  maxWidth?: number;
  maxHeight?: number;
}

export interface FileValidationResult {
  isValid: boolean;
  error?: string;
}

export const validateFileType = async (
  file: File,
  config: FileTypeConfig
): Promise<FileValidationResult> => {
  // Check file extension
  const extension = `.${file.name.split('.').pop()?.toLowerCase()}`;
  if (!config.accept.includes(extension)) {
    return {
      isValid: false,
      error: `Invalid file type. Accepted types: ${config.accept.join(', ')}`
    };
  }
  
  // Check file size
  if (config.maxSize && file.size > config.maxSize) {
    return {
      isValid: false,
      error: `File too large. Maximum size: ${formatBytes(config.maxSize)}`
    };
  }
  
  if (config.minSize && file.size < config.minSize) {
    return {
      isValid: false,
      error: `File too small. Minimum size: ${formatBytes(config.minSize)}`
    };
  }
  
  // Check image dimensions
  if (file.type.startsWith('image/') && (config.maxWidth || config.maxHeight)) {
    try {
      const dimensions = await getImageDimensions(file);
      
      if (config.maxWidth && dimensions.width > config.maxWidth) {
        return {
          isValid: false,
          error: `Image width must be at most ${config.maxWidth}px`
        };
      }
      
      if (config.maxHeight && dimensions.height > config.maxHeight) {
        return {
          isValid: false,
          error: `Image height must be at most ${config.maxHeight}px`
        };
      }
    } catch {
      return {
        isValid: false,
        error: 'Failed to validate image dimensions'
      };
    }
  }
  
  return { isValid: true };
};

/**
 * Get image dimensions
 */
const getImageDimensions = (file: File): Promise<{ width: number; height: number }> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({
        width: img.width,
        height: img.height
      });
    };
    img.onerror = reject;
    img.src = URL.createObjectURL(file);
  });
};
```

### Chat Validation
```typescript
/**
 * Validate chat import data
 */
export interface ChatImportValidation {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export const validateChatImport = (data: any): ChatImportValidation => {
  const result: ChatImportValidation = {
    isValid: true,
    errors: [],
    warnings: []
  };
  
  // Check required fields
  if (!data.messages || !Array.isArray(data.messages)) {
    result.errors.push('Missing or invalid messages array');
    result.isValid = false;
  }
  
  // Check message format
  if (data.messages) {
    data.messages.forEach((message: any, index: number) => {
      if (!message.content) {
        result.errors.push(`Message ${index + 1}: Missing content`);
        result.isValid = false;
      }
      
      if (!message.sender) {
        result.errors.push(`Message ${index + 1}: Missing sender`);
        result.isValid = false;
      }
      
      if (!message.timestamp) {
        result.warnings.push(`Message ${index + 1}: Missing timestamp`);
      }
    });
  }
  
  // Check platform
  if (!data.platform) {
    result.warnings.push('Missing platform information');
  }
  
  return result;
};

/**
 * Validate chat message
 */
export interface MessageValidation {
  isValid: boolean;
  error?: string;
}

export const validateMessage = (message: string): MessageValidation => {
  if (!message.trim()) {
    return {
      isValid: false,
      error: 'Message cannot be empty'
    };
  }
  
  if (message.length > 10000) {
    return {
      isValid: false,
      error: 'Message too long (max 10000 characters)'
    };
  }
  
  return { isValid: true };
};
```

### Guest Limits Validation
```typescript
/**
 * Validate guest user limits
 */
export interface GuestLimits {
  maxImports: number;
  maxMessages: number;
  imports: number;
  messages: number;
}

export interface GuestLimitsValidation {
  canImport: boolean;
  canMessage: boolean;
  remainingImports: number;
  remainingMessages: number;
}

export const validateGuestLimits = (limits: GuestLimits): GuestLimitsValidation => {
  return {
    canImport: limits.imports < limits.maxImports,
    canMessage: limits.messages < limits.maxMessages,
    remainingImports: limits.maxImports - limits.imports,
    remainingMessages: limits.maxMessages - limits.messages
  };
};
```

## Usage Examples

### Form Validation
```typescript
// Email validation
console.log(isValidEmail('user@example.com'));
// Output: true

console.log(isValidEmail('invalid-email'));
// Output: false

// Password validation
const passwordStrength = validatePassword('MyPassword123!');
console.log(passwordStrength);
// Output: {
//   isValid: true,
//   score: 100,
//   feedback: []
// }

// Field validation
const nameRules = {
  required: true,
  minLength: 2,
  maxLength: 50
};

console.log(validateField('', nameRules));
// Output: 'This field is required'

console.log(validateField('A', nameRules));
// Output: 'Minimum length is 2 characters'
```

### File Validation
```typescript
const imageConfig = {
  accept: ['.jpg', '.jpeg', '.png'],
  maxSize: 5 * 1024 * 1024, // 5MB
  maxWidth: 1920,
  maxHeight: 1080
};

const file = new File([''], 'image.jpg', { type: 'image/jpeg' });
const result = await validateFileType(file, imageConfig);

console.log(result);
// Output: { isValid: true }
```

### Chat Validation
```typescript
// Chat import validation
const importData = {
  messages: [
    {
      content: 'Hello',
      sender: 'user',
      timestamp: '2025-03-27T12:34:56Z'
    }
  ],
  platform: 'chatgpt'
};

console.log(validateChatImport(importData));
// Output: {
//   isValid: true,
//   errors: [],
//   warnings: []
// }

// Message validation
console.log(validateMessage('Hello, world!'));
// Output: { isValid: true }

console.log(validateMessage(''));
// Output: {
//   isValid: false,
//   error: 'Message cannot be empty'
// }
```

### Guest Limits Validation
```typescript
const guestLimits = {
  maxImports: 2,
  maxMessages: 5,
  imports: 1,
  messages: 3
};

console.log(validateGuestLimits(guestLimits));
// Output: {
//   canImport: true,
//   canMessage: true,
//   remainingImports: 1,
//   remainingMessages: 2
// }
```
