// src/components/Navbar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icons } from './Icons';
import clsx from 'clsx';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
    const pathname = usePathname();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const navItems = [
        { name: 'Portal', href: '/', icon: Icons.Galaxy },
        { name: 'Sandbox', href: '/sandbox', icon: Icons.Time },
        { name: 'Governance', href: '/governance', icon: Icons.Governance },
        { name: 'War Room', href: '/war-room', icon: Icons.WarRoom },
    ];

    return (
        <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-black/70 backdrop-blur-xl shadow-lg shadow-black/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <motion.div
                        className="flex items-center"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <Link href="/" className="flex items-center space-x-2 group">
                            <motion.div
                                whileHover={{ rotate: 360 }}
                                transition={{ duration: 0.6 }}
                            >
                                <Icons.Brain className="h-8 w-8 text-primary transition-all duration-300 group-hover:drop-shadow-[0_0_8px_rgba(102,252,241,0.6)]" />
                            </motion.div>
                            <span className="text-xl font-bold tracking-wider text-white group-hover:text-primary transition-colors duration-300">WEION</span>
                        </Link>
                    </motion.div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:block">
                        <div className="ml-10 flex items-baseline space-x-2">
                            {navItems.map((item, index) => {
                                const isActive = pathname === item.href;
                                const Icon = item.icon;
                                return (
                                    <motion.div
                                        key={item.name}
                                        initial={{ opacity: 0, y: -10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                    >
                                        <Link
                                            href={item.href}
                                            className={clsx(
                                                'relative flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 group',
                                                isActive
                                                    ? 'bg-primary/20 text-primary shadow-[0_0_15px_rgba(102,252,241,0.3)] backdrop-blur-sm'
                                                    : 'text-gray-400 hover:text-white hover:bg-white/10 hover:backdrop-blur-sm'
                                            )}
                                        >
                                            <Icon className={clsx(
                                                "h-4 w-4 transition-all duration-300",
                                                isActive ? "drop-shadow-[0_0_4px_rgba(102,252,241,0.8)]" : "group-hover:scale-110"
                                            )} />
                                            <span>{item.name}</span>
                                            {isActive && (
                                                <motion.div
                                                    layoutId="activeTab"
                                                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-full"
                                                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                                                />
                                            )}
                                        </Link>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Mobile Menu Button */}
                    <motion.button
                        className="md:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-all duration-300"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        whileTap={{ scale: 0.95 }}
                    >
                        <motion.div
                            animate={mobileMenuOpen ? "open" : "closed"}
                            className="w-6 h-6 flex flex-col justify-around"
                        >
                            <motion.span
                                variants={{
                                    closed: { rotate: 0, y: 0 },
                                    open: { rotate: 45, y: 8 }
                                }}
                                className="w-full h-0.5 bg-current rounded-full transform origin-center transition-all duration-300"
                            />
                            <motion.span
                                variants={{
                                    closed: { opacity: 1 },
                                    open: { opacity: 0 }
                                }}
                                className="w-full h-0.5 bg-current rounded-full transition-all duration-300"
                            />
                            <motion.span
                                variants={{
                                    closed: { rotate: 0, y: 0 },
                                    open: { rotate: -45, y: -8 }
                                }}
                                className="w-full h-0.5 bg-current rounded-full transform origin-center transition-all duration-300"
                            />
                        </motion.div>
                    </motion.button>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="md:hidden border-t border-white/10 bg-black/90 backdrop-blur-xl overflow-hidden"
                    >
                        <div className="px-4 py-4 space-y-2">
                            {navItems.map((item, index) => {
                                const isActive = pathname === item.href;
                                const Icon = item.icon;
                                return (
                                    <motion.div
                                        key={item.name}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        transition={{ delay: index * 0.05 }}
                                    >
                                        <Link
                                            href={item.href}
                                            onClick={() => setMobileMenuOpen(false)}
                                            className={clsx(
                                                'flex items-center space-x-3 px-4 py-3 rounded-lg text-base font-medium transition-all duration-300',
                                                isActive
                                                    ? 'bg-primary/20 text-primary shadow-[0_0_15px_rgba(102,252,241,0.2)]'
                                                    : 'text-gray-400 hover:text-white hover:bg-white/10'
                                            )}
                                        >
                                            <Icon className="h-5 w-5" />
                                            <span>{item.name}</span>
                                        </Link>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}
