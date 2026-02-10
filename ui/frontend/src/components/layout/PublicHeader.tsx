"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

const links = [
    { href: "/product", label: "Product" },
    { href: "/use-cases", label: "Solutions" },
    { href: "/pricing", label: "Pricing" },
    { href: "/contact", label: "Contact" },
];

export function PublicHeader() {
    return (
        <header className="fixed top-0 w-full z-50 border-b bg-background/80 backdrop-blur-xl">
            <div className="container mx-auto px-6 h-16 flex items-center justify-between">
                <Link href="/" className="flex items-center gap-2 font-bold text-lg tracking-tight">
                    <div className="w-6 h-6 bg-foreground text-background rounded flex items-center justify-center text-xs">W</div>
                    WEION
                </Link>

                <nav className="hidden md:flex items-center gap-8">
                    {links.map((link) => (
                        <Link
                            key={link.href}
                            href={link.href}
                            className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                        >
                            {link.label}
                        </Link>
                    ))}
                </nav>

                <div className="flex items-center gap-4">
                    <Link href="/login" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                        Log in
                    </Link>
                    <Button size="sm" className="h-8 px-4 text-xs">
                        <Link href="/signup">Get Started</Link>
                    </Button>
                </div>
            </div>
        </header>
    );
}
