/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#2E3E7E',
        secondary: '#E6B422',
      },
    },
  },
  plugins: [],
  important: true, // TailwindのクラスがMUIのスタイルより優先されるようにする
};
