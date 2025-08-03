"use client";

import React from 'react';
import Link from 'next/link';
import { LanguageProvider, useLanguage } from '../i18n/LanguageContext';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import privacyContent from './content.md';

export default function PrivacyPolicy() {
    return (
        <LanguageProvider>
            <PrivacyPolicyContent />
        </LanguageProvider>
    );
}

function PrivacyPolicyContent() {
    const { language, setLanguage, t, isRTL } = useLanguage();

    const languageOptions = [
        { code: 'en', name: 'English', flag: '🇺🇸' },
        { code: 'zh', name: '中文', flag: '🇨🇳' },
        { code: 'ar', name: 'العربية', flag: '🇸🇦' },
        { code: 'es', name: 'Español', flag: '🇪🇸' },
        { code: 'pt', name: 'Português', flag: '🇧🇷' }
    ];

    return (
        <div className={`min-h-screen bg-black text-white overflow-hidden ${isRTL ? 'rtl' : 'ltr'}`}>
            {/* Animated Background */}
            <div className="fixed inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
                <div className="absolute inset-0 opacity-20 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%239C92AC%22%20fill-opacity%3D%220.05%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%222%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')]"></div>
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 animate-pulse"></div>
            </div>

            {/* Header */}
            <header className="relative z-10 w-full bg-black/20 backdrop-blur-xl border-b border-white/10">
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <nav className="flex justify-between items-center">
                        {/* Logo */}
                        <div className="flex items-center space-x-3">
                            <Link href="/" className="flex items-center space-x-3">
                                <div className="relative">
                                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-2xl animate-pulse">
                                        <span className="text-white text-xl font-bold">I</span>
                                    </div>
                                    <div className="absolute -inset-1 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-2xl blur opacity-30 animate-pulse"></div>
                                </div>
                                <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
                                    {t.hero.title}
                                </span>
                            </Link>
                        </div>

                        {/* Navigation */}
                        <div className="hidden md:flex items-center space-x-8">
                            <Link href="/#features" className="text-gray-300 hover:text-white transition-colors font-medium relative group">
                                {t.nav.features}
                                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 group-hover:w-full transition-all duration-300"></span>
                            </Link>
                            <Link href="/#pricing" className="text-gray-300 hover:text-white transition-colors font-medium relative group">
                                {t.nav.pricing}
                                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-purple-400 to-pink-400 group-hover:w-full transition-all duration-300"></span>
                            </Link>
                            <Link href="/#about" className="text-gray-300 hover:text-white transition-colors font-medium relative group">
                                {t.nav.about}
                                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-pink-400 to-blue-400 group-hover:w-full transition-all duration-300"></span>
                            </Link>
                        </div>

                        {/* Right side */}
                        <div className="flex items-center space-x-4">
                            <select
                                className="bg-black/30 border border-white/20 rounded-xl px-4 py-2 text-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm backdrop-blur-sm"
                                value={language}
                                onChange={(e) => setLanguage(e.target.value as 'en' | 'zh' | 'ar' | 'es' | 'pt')}
                            >
                                {languageOptions.map((option) => (
                                    <option key={option.code} value={option.code}>
                                        {option.flag} {option.name}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="relative z-10 pt-8 pb-16">
                <div className="max-w-4xl mx-auto px-6">
                    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl p-8 md:p-12">
                        <div className="prose prose-invert prose-lg max-w-none">
                            <div className="text-gray-300">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        h1: ({ children }) => (
                                            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-8">
                                                {children}
                                            </h1>
                                        ),
                                        h2: ({ children }) => (
                                            <h2 className="text-3xl font-bold text-white mt-12 mb-6">
                                                {children}
                                            </h2>
                                        ),
                                        h3: ({ children }) => (
                                            <h3 className="text-2xl font-bold text-white mt-8 mb-4">
                                                {children}
                                            </h3>
                                        ),
                                        p: ({ children }) => (
                                            <p className="text-gray-300 mb-4 leading-relaxed">
                                                {children}
                                            </p>
                                        ),
                                        ul: ({ children }) => (
                                            <ul className="list-disc list-inside text-gray-300 mb-4 space-y-2">
                                                {children}
                                            </ul>
                                        ),
                                        li: ({ children }) => (
                                            <li className="text-gray-300">
                                                {children}
                                            </li>
                                        ),
                                        strong: ({ children }) => (
                                            <strong className="font-semibold text-white">
                                                {children}
                                            </strong>
                                        ),
                                        a: ({ href, children }) => (
                                            <a
                                                href={href}
                                                className="text-blue-400 hover:text-blue-300 underline transition-colors"
                                                target="_blank"
                                                rel="noopener noreferrer"
                                            >
                                                {children}
                                            </a>
                                        ),
                                        hr: () => (
                                            <hr className="border-gray-600 my-8" />
                                        ),
                                    }}
                                >
                                    {privacyContent}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="relative z-10 w-full bg-black/20 backdrop-blur-xl border-t border-white/10 py-8 mt-16">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="flex flex-col md:flex-row justify-between items-center">
                        {/* Copyright */}
                        <div className="text-gray-400 text-sm mb-4 md:mb-0">
                            © {new Date().getFullYear()} Imagint Labs. All rights reserved.
                        </div>

                        {/* Links */}
                        <div className="flex items-center space-x-6">
                            <Link
                                href="/privacy-policy"
                                className="text-gray-400 hover:text-white transition-colors text-sm"
                            >
                                Privacy Policy
                            </Link>
                            <Link
                                href="/terms-of-service"
                                className="text-gray-400 hover:text-white transition-colors text-sm"
                            >
                                Terms of Service
                            </Link>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
} 