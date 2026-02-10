
// src/app/layout.tsx
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Navbar from '@/components/Navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'WEION | Governed Intelligence',
    description: 'The Civilization Engine. A Sovereign AI Architecture.',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <Navbar />
                <main className="pt-16 min-h-screen">
                    {children}
                </main>
            </body>
        </html>
    )
}
