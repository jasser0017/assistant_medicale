/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#3B82F6",
        secondary: "#6366F1",
        background: "#0F172A",
        bgLight: "#F0F5FF",
        whiteGlass: "rgba(255,255,255,0.2)",
        medical: {
          gray: '#F8FAFC',
          slate: '#64748B',
          border: '#E2E8F0'
        }
      },
      backdropBlur: {
        xs: "2px",
      },
      borderRadius: {
        "4xl": "2rem",
      },
      boxShadow: {
        soft: '0 4px 24px rgba(0, 0, 0, 0.08)',
        hover: '0 8px 32px rgba(0, 0, 0, 0.12)'
      }

    },
  },
  plugins: [require("@tailwindcss/forms")],
};