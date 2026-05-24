/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/**/*.html",
    "./billing/**/*.py",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Manrope", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#d8e4ff",
          200: "#b8cdff",
          300: "#8daeff",
          400: "#5d86fc",
          500: "#395fe9",
          600: "#2f4cc8",
          700: "#273da1",
          800: "#243684",
          900: "#22306d",
        },
      },
      boxShadow: {
        soft: "0 6px 20px rgba(15, 23, 42, 0.06)",
      },
    },
  },
  plugins: [],
};
