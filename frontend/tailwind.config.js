/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tg_bg: 'var(--tg-theme-bg-color, #ffffff)',
        tg_text: 'var(--tg-theme-text-color, #000000)',
        tg_hint: 'var(--tg-theme-hint-color, #999999)',
        tg_link: 'var(--tg-theme-link-color, #2481cc)',
        tg_primary: 'var(--tg-theme-button-color, #5288c1)',
        tg_primary_text: 'var(--tg-theme-button-text-color, #ffffff)',
        tg_secondary_bg: 'var(--tg-theme-secondary-bg-color, #efeff3)',
      }
    },
  },
  plugins: [],
}
