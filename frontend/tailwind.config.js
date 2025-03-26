/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Primary palette (from first link)
        primary: {
          100: '#DDE6ED',
          200: '#9DB2BF',
          300: '#526D82',
          400: '#27374D',
        },
        // Secondary palette (from second link)
        secondary: {
          100: '#9EC8B9',
          200: '#5C8374',
          300: '#1B4242',
          400: '#092635',
        },
        // Accent palette (from third link)
        accent: {
          100: '#E2F4C5',
          200: '#A8CD9F',
          300: '#58A399',
          400: '#496989',
        },
        // Semantic colors
        background: {
          DEFAULT: '#DDE6ED', // primary-100
          dark: '#27374D',    // primary-400
        },
        surface: {
          DEFAULT: '#FFFFFF',
          dark: '#526D82',    // primary-300
        },
        text: {
          DEFAULT: '#27374D', // primary-400
          light: '#9DB2BF',   // primary-200
          dark: '#DDE6ED',    // primary-100
        },
        border: {
          DEFAULT: '#9DB2BF', // primary-200
          dark: '#526D82',    // primary-300
        },
        success: '#58A399',   // accent-300
        error: '#E11D48',
        warning: '#F59E0B',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-in-out',
        'slide-down': 'slideDown 0.5s ease-in-out',
        'slide-left': 'slideLeft 0.5s ease-in-out',
        'slide-right': 'slideRight 0.5s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideLeft: {
          '0%': { transform: 'translateX(20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        slideRight: {
          '0%': { transform: 'translateX(-20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(to right, #27374D, #526D82)',
        'gradient-secondary': 'linear-gradient(to right, #092635, #1B4242)',
        'gradient-accent': 'linear-gradient(to right, #496989, #58A399)',
      }
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
