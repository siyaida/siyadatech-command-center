/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0f',
        foreground: '#f0f0f5',
        card: '#13131f',
        border: '#252536',
        accent: '#8b5cf6',
        'accent-light': '#a78bfa',
      },
    },
  },
  plugins: [],
}