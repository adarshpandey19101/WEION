"use client";

import Link from "next/link";
import { Github, Twitter, Linkedin } from "lucide-react";

const footerLinks = {
    Product: [
        { label: "Features", href: "/product" },
        { label: "Security", href: "/security" },
        { label: "Enterprise", href: "/use-cases" },
        { label: "Pricing", href: "/pricing" },
    ],
    Resources: [
        { label: "Documentation", href: "#" },
        { label: "API Reference", href: "#" },
        { label: "Blog", href: "#" },
        { label: "Status", href: "#" },
    ],
    Company: [
        { label: "About", href: "#" },
        { label: "Careers", href: "#" },
        { label: "Legal", href: "/trust" },
        { label: "Contact", href: "/contact" },
    ],
};

export function PublicFooter() {
    return (
        <footer className="border-t bg-background py-12 md:py-16 lg:py-20">
            <div className="container mx-auto px-6 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
                <div className="col-span-2 lg:col-span-2 space-y-4">
                    <Link href="/" className="flex items-center gap-2 font-bold text-lg tracking-tight">
                        <div className="w-6 h-6 bg-foreground text-background rounded flex items-center justify-center text-xs">W</div>
                        WEION
                    </Link>
                    <p className="text-sm text-muted-foreground max-w-xs">
                        The Enterprise Cognitive Operating System. Autonomous, auditable, and aligned with human values.
                    </p>
                    <div className="flex gap-4">
                        <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                            <Twitter className="w-5 h-5" />
                        </Link>
                        <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                            <Github className="w-5 h-5" />
                        </Link>
                        <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                            <Linkedin className="w-5 h-5" />
                        </Link>
                    </div>
                </div>

                {Object.entries(footerLinks).map(([category, links]) => (
                    <div key={category} className="space-y-4">
                        <h4 className="text-sm font-semibold">{category}</h4>
                        <ul className="space-y-2">
                            {links.map((link) => (
                                <li key={link.label}>
                                    <Link href={link.href} className="text-xs text-muted-foreground hover:text-foreground transition-colors">
                                        {link.label}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            <div className="container mx-auto px-6 mt-12 pt-8 border-t text-xs text-muted-foreground flex flex-col md:flex-row justify-between items-center gap-4">
                <p>© 2024 WEION Inc. All rights reserved.</p>
                <div className="flex gap-4">
                    <Link href="#" className="hover:text-foreground">Privacy Policy</Link>
                    <Link href="#" className="hover:text-foreground">Terms of Service</Link>
                </div>
            </div>
        </footer>
    );
}
