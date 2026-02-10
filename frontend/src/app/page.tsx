// src/app/page.tsx
'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Icons } from '@/components/Icons';

export default function Home() {
    const cards = [
        {
            title: "Sandbox",
            href: "/sandbox",
            icon: Icons.Galaxy,
            description: "Explore AI capabilities in a controlled environment",
            gradient: "from-blue-900/40 via-blue-800/30 to-blue-900/40",
            borderColor: "border-blue-500/30",
            hoverBorderColor: "hover:border-blue-400/60",
            iconColor: "text-blue-400",
            glowColor: "group-hover:shadow-[0_0_30px_rgba(59,130,246,0.3)]"
        },
        {
            title: "Governance",
            href: "/governance",
            icon: Icons.Governance,
            description: "View constitutional principles and voting history",
            gradient: "from-purple-900/40 via-purple-800/30 to-purple-900/40",
            borderColor: "border-purple-500/30",
            hoverBorderColor: "hover:border-purple-400/60",
            iconColor: "text-purple-400",
            glowColor: "group-hover:shadow-[0_0_30px_rgba(168,85,247,0.3)]"
        },
        {
            title: "War Room",
            href: "/war-room",
            icon: Icons.WarRoom,
            description: "Monitor live AI decision-making processes",
            gradient: "from-green-900/40 via-green-800/30 to-green-900/40",
            borderColor: "border-green-500/30",
            hoverBorderColor: "hover:border-green-400/60",
            iconColor: "text-green-400",
            glowColor: "group-hover:shadow-[0_0_30px_rgba(34,197,94,0.3)]"
        }
    ];

    return (
        <div className="min-h-screen flex flex-col justify-center items-center p-4 sm:p-8 relative overflow-hidden bg-gradient-to-br from-black via-gray-900 to-black text-white">

            {/* Animated Background Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(102,252,241,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(102,252,241,0.03)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,black,transparent)]" />

            {/* Hero Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="max-w-5xl mx-auto text-center space-y-8 sm:space-y-12 z-10 px-4"
            >
                {/* Title Section */}
                <div className="space-y-4 sm:space-y-6">
                    <motion.h1
                        className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                    >
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 animate-gradient bg-[length:200%_auto]">
                            WEION
                        </span>
                    </motion.h1>

                    <motion.p
                        className="text-xl sm:text-2xl md:text-3xl text-gray-300 font-light"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.8, delay: 0.4 }}
                    >
                        Governed Intelligence
                    </motion.p>

                    <motion.p
                        className="text-sm sm:text-base md:text-lg text-gray-400 max-w-2xl mx-auto px-4"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.8, delay: 0.6 }}
                    >
                        A next-generation AI governance framework ensuring ethical, transparent, and accountable artificial intelligence systems.
                    </motion.p>
                </div>

                {/* Navigation Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mt-8 sm:mt-12 px-2 sm:px-4">
                    {cards.map((card, index) => {
                        const Icon = card.icon;
                        return (
                            <motion.div
                                key={card.title}
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{
                                    duration: 0.6,
                                    delay: 0.8 + (index * 0.15),
                                    ease: [0.22, 1, 0.36, 1]
                                }}
                            >
                                <Link href={card.href}>
                                    <motion.div
                                        whileHover={{ y: -8, scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                        className={`group relative p-6 sm:p-8 bg-gradient-to-br ${card.gradient} border ${card.borderColor} ${card.hoverBorderColor} rounded-2xl cursor-pointer transition-all duration-500 backdrop-blur-sm ${card.glowColor} overflow-hidden`}
                                    >
                                        {/* Glow Effect */}
                                        <div className={`absolute inset-0 bg-gradient-to-br ${card.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl`} />

                                        {/* Content */}
                                        <div className="relative z-10 flex flex-col items-center text-center space-y-4">
                                            <motion.div
                                                whileHover={{ rotate: 360 }}
                                                transition={{ duration: 0.6 }}
                                                className="p-4 rounded-full bg-black/30 backdrop-blur-sm group-hover:bg-black/50 transition-all duration-300"
                                            >
                                                <Icon className={`h-10 w-10 sm:h-12 sm:w-12 ${card.iconColor} drop-shadow-[0_0_8px_currentColor] group-hover:drop-shadow-[0_0_16px_currentColor] transition-all duration-300`} />
                                            </motion.div>

                                            <h3 className="text-xl sm:text-2xl font-bold text-white group-hover:scale-105 transition-transform duration-300">
                                                {card.title}
                                            </h3>

                                            <p className="text-xs sm:text-sm text-gray-400 group-hover:text-gray-300 transition-colors duration-300 leading-relaxed">
                                                {card.description}
                                            </p>
                                        </div>

                                        {/* Corner Accent */}
                                        <div className={`absolute top-0 right-0 w-20 h-20 bg-gradient-to-br ${card.gradient} opacity-20 blur-2xl group-hover:opacity-40 transition-opacity duration-500`} />
                                    </motion.div>
                                </Link>
                            </motion.div>
                        );
                    })}
                </div>

                {/* Floating Particles Effect */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    {[...Array(20)].map((_, i) => (
                        <motion.div
                            key={i}
                            className="absolute w-1 h-1 bg-primary/30 rounded-full"
                            initial={{
                                x: Math.random() * window.innerWidth,
                                y: Math.random() * window.innerHeight,
                                scale: Math.random() * 0.5 + 0.5
                            }}
                            animate={{
                                y: [null, Math.random() * window.innerHeight],
                                opacity: [0, 1, 0],
                            }}
                            transition={{
                                duration: Math.random() * 10 + 10,
                                repeat: Infinity,
                                ease: "linear"
                            }}
                        />
                    ))}
                </div>
            </motion.div>
        </div>
    );
}
