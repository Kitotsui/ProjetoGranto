/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.css',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#322d70',
        secondary: '#2b452b',
        accent: '#01080e',
      },
    },
  },
  plugins: [],
}
