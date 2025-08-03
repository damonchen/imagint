"use client";

import React from 'react';
import Link from 'next/link';

export default function Dashboard() {
    return (
        <div className="min-h-screen bg-black text-white">
            <div className="max-w-4xl mx-auto px-6 py-12">
                <div className="text-center">
                    <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-6">
                        Welcome to Dashboard
                    </h1>
                    <p className="text-xl text-gray-300 mb-8">
                        You have successfully upgraded your plan!
                    </p>

                    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 mb-8">
                        <h2 className="text-2xl font-bold text-white mb-4">Your Plan Features</h2>
                        <ul className="space-y-3 text-gray-300">
                            <li className="flex items-center">
                                <svg className="w-5 h-5 text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                                </svg>
                                Unlimited image generation
                            </li>
                            <li className="flex items-center">
                                <svg className="w-5 h-5 text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                                </svg>
                                High resolution images (up to 4K)
                            </li>
                            <li className="flex items-center">
                                <svg className="w-5 h-5 text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                                </svg>
                                Priority support
                            </li>
                            <li className="flex items-center">
                                <svg className="w-5 h-5 text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                                </svg>
                                Advanced editing tools
                            </li>
                        </ul>
                    </div>

                    <Link
                        href="/"
                        className="inline-block px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white rounded-xl font-semibold transition-all duration-200"
                    >
                        Back to Home
                    </Link>
                </div>
            </div>
        </div>
    );
} 