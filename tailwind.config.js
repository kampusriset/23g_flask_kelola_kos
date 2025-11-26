/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class", // <--- penting!
  content: [
    "./app/templates/**/*.html",
    "./app/static/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
