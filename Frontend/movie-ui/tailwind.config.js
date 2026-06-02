/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00d9ff',
        secondary: '#0f172a',
        card: '#111827',
      },
      boxShadow: {
        neon: '0 0 15px rgba(0,217,255,0.6)',
      },
    },
  },
  plugins: [],
}