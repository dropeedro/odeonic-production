/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Estilos viejos
        primaryPurpleColor: '#82328b',
        secondaryWhiteColor: '#f9f9f9',
        terciaryPurpleColor: '#762D7E',
        // Estilos Nuevos
        PrimaryColor: '#FFDE59',
        PrimaryColorDark: '#E5C750',
        SecondaryColor: '#142730',
        SecondaryColorDark: '#12232B',
        LightColor: '#f9f9f9',

        plusGrayColor: '#D9D9D9',
        backgroundColor: '#FFFFFF',
      }
    },
  },
  plugins: [],
}