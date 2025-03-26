# tailwind.config.js

## Purpose
This configuration file defines the styling system for VoxStitch's frontend. It extends Tailwind CSS with custom colors, fonts, animations, and other design tokens to create a consistent design language throughout the application.

## Key Features

### Color Palette System
The configuration defines semantic color tokens that map to specific design values:

- **Primary Colors**: A range of blues and teals used for primary UI elements
- **Surface Colors**: Background colors for different UI layers and cards
- **Text Colors**: Typography colors with different emphasis levels
- **Border Colors**: Used for dividers and container outlines
- **Status Colors**: For success, error, warning and information states

### Gradient Definitions
The configuration defines custom gradients that are used throughout the application:
- `gradient-primary`: Used for buttons, active states, and focus indicators
- `gradient-surface`: Used for card and panel backgrounds
- `gradient-accent`: Used for highlighting important UI elements

### Spacing and Sizing
Custom spacing and sizing scales ensure consistent layout throughout the application, with a responsive design system that adapts to different screen sizes.

### Typography System
Defines font families, weights, sizes, and line heights to create a typographic hierarchy that guides users through the interface.

### Custom Components
The configuration supports custom component styling through extended theme values, particularly for:
- Buttons with different variants (primary, outline, ghost)
- Form elements (inputs, selects, checkboxes)
- Cards and dialogs

## Integration with Design System
The configuration values are referenced throughout the application's component styles to maintain consistency. This file is a central source of truth for the design system.

## Relation to Other Files
- Used by all styled components in the application
- Referenced by style utilities for generating dynamic styles
- Works with PostCSS plugins to optimize the final CSS bundle

## Recent Updates
The configuration was recently updated to implement a more modern gradient-based design system that replaces solid colors, creating a more visually appealing interface with depth and dimension.
