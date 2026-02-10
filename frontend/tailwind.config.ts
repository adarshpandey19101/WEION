import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#0B0C10", // Obsidian Black
                surface: "#1F2833",    // Dark Charcoal
                primary: "#66FCF1",    // Neon Cyan
                secondary: "#45A29E",  // Muted Teal
                text: "#C5C6C7",       // Starlight Silver
                accent: "#C5C6C7",
            },
            fontFamily: {
                mono: ['Inter', 'monospace'],
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
            },
            animation: {
                'gradient': 'gradient 8s linear infinite',
            },
            keyframes: {
                gradient: {
                    '0%, 100%': {
                        'background-position': '0% 50%',
                    },
                    '50%': {
                        'background-position': '100% 50%',
                    },
                },
            },
        },
    },
    plugins: [],
};
export default config;
