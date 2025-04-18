/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8B5CF6',
          dark: '#6D28D9',
        },
        secondary: {
          DEFAULT: '7AE2CF',
          light: '7AE2CF',
          deep: '7AE2CF',
        }
      }
    },
  },
  plugins: [],
};