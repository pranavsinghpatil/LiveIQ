# ChatSynth Design System

## Color Palette

### Primary Colors
```css
--primary-100: #E6F3FF;  /* Light background */
--primary-200: #B3D9FF;  /* Hover states */
--primary-300: #80BFFF;  /* Active states */
--primary-400: #4DA6FF;  /* Secondary buttons */
--primary-500: #1A8CFF;  /* Primary buttons */
--primary-600: #0073E6;  /* Text on light */
--primary-700: #005BB3;  /* Headers */
--primary-800: #004280;  /* Dark accents */
```

### Neutral Colors
```css
--neutral-100: #FFFFFF;  /* Background */
--neutral-200: #F5F5F5;  /* Cards, sections */
--neutral-300: #E0E0E0;  /* Borders */
--neutral-400: #BDBDBD;  /* Disabled */
--neutral-500: #9E9E9E;  /* Placeholder text */
--neutral-600: #757575;  /* Secondary text */
--neutral-700: #616161;  /* Body text */
--neutral-800: #424242;  /* Headers */
--neutral-900: #212121;  /* Dark text */
```

### Semantic Colors
```css
--success: #4CAF50;  /* Success states */
--warning: #FFC107;  /* Warning states */
--error: #F44336;    /* Error states */
--info: #2196F3;     /* Info states */
```

### Platform Colors
```css
--chatgpt: #19C37D;   /* ChatGPT content */
--mistral: #7C3AED;   /* Mistral content */
--gemini: #1A73E8;    /* Gemini content */
```

## Typography

### Font Families
```css
--font-primary: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

## Spacing

### Base Units
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

## Borders & Shadows

### Border Radius
```css
--radius-sm: 0.125rem;    /* 2px */
--radius-base: 0.25rem;   /* 4px */
--radius-md: 0.375rem;    /* 6px */
--radius-lg: 0.5rem;      /* 8px */
--radius-xl: 0.75rem;     /* 12px */
--radius-2xl: 1rem;       /* 16px */
--radius-full: 9999px;    /* Full round */
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

## Component Base Styles

### Buttons
```css
.btn {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-base);
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--primary-500);
  color: white;
}

.btn-secondary {
  background: var(--primary-100);
  color: var(--primary-600);
}

.btn-outline {
  border: 1px solid var(--neutral-300);
  color: var(--neutral-700);
}
```

### Input Fields
```css
.input {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--neutral-300);
  border-radius: var(--radius-base);
  font-size: var(--text-base);
  transition: border-color 0.2s ease;
}

.input:focus {
  border-color: var(--primary-500);
  outline: none;
  box-shadow: 0 0 0 2px var(--primary-100);
}
```

### Cards
```css
.card {
  background: var(--neutral-100);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-base);
}
```

## Responsive Breakpoints
```css
--screen-sm: 640px;   /* Small devices */
--screen-md: 768px;   /* Medium devices */
--screen-lg: 1024px;  /* Large devices */
--screen-xl: 1280px;  /* Extra large devices */
--screen-2xl: 1536px; /* 2X Extra large devices */
```

## Animation
```css
--transition-base: all 0.2s ease;
--transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
--transition-bounce: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
```
