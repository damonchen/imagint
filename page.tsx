"use client";

import Image from "next/image";
import React, { useState, useEffect, useRef } from "react";
import { LanguageProvider, useLanguage } from './i18n/LanguageContext';
import axios from 'axios';
import { API_ENDPOINTS } from '../config/env';
import { logEnvironmentValidation } from '../utils/envValidator';

export default function Home() {
  return (
    <LanguageProvider>
      <HomeContent />
    </LanguageProvider>
  );
}

function HomeContent() {
  const { language, setLanguage, t, isRTL } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [showSignInModal, setShowSignInModal] = useState(false);
  const [activeFAQ, setActiveFAQ] = useState<number | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false); // 模拟用户登录状态
  const [upgradingPlan, setUpgradingPlan] = useState<string | null>(null);

    useEffect(() => {
    // Validate environment variables
    logEnvironmentValidation();
    
    // 模拟加载过程
    const timer = setTimeout(() => {
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, []);

  // 处理定价按钮点击
  const handlePricingClick = (planName: string) => {
    if (planName === t.pricing.enterprise) {
      // 企业版：发送邮件
      const subject = encodeURIComponent('Enterprise Plan Inquiry');
      const body = encodeURIComponent('Hello,\n\nI am interested in your Enterprise plan. Please provide more information about pricing and features.\n\nBest regards,');
      window.location.href = `mailto:sales@imagint.ai?subject=${subject}&body=${body}`;
    } else {
      // Premium 和 Ultimate 计划
      if (!isLoggedIn) {
        // 未登录：显示登录提示
        setShowSignInModal(true);
      } else {
        // 已登录：显示升级状态并跳转到后台
        setUpgradingPlan(planName);
        setTimeout(() => {
          // 模拟跳转到后台页面
          window.location.href = '/dashboard';
        }, 2000);
      }
    }
  };

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
              <div className="relative">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-2xl animate-pulse">
                  <span className="text-white text-xl font-bold">I</span>
                </div>
                <div className="absolute -inset-1 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-2xl blur opacity-30 animate-pulse"></div>
              </div>
              <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
                {t.hero.title}
              </span>
            </div>

            {/* Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-300 hover:text-white transition-colors font-medium relative group">
                {t.nav.features}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 group-hover:w-full transition-all duration-300"></span>
              </a>
              <a href="#pricing" className="text-gray-300 hover:text-white transition-colors font-medium relative group">
                {t.nav.pricing}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-purple-400 to-pink-400 group-hover:w-full transition-all duration-300"></span>
              </a>
              <a href="#about" className="text-gray-300 hover:text-white transition-colors font-medium relative group">
                {t.nav.about}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-pink-400 to-blue-400 group-hover:w-full transition-all duration-300"></span>
              </a>
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

              <button
                onClick={() => setShowSignInModal(true)}
                className="relative px-6 py-2 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 overflow-hidden group"
              >
                <span className="relative z-10">{t.nav.signIn}</span>
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
              </button>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10">
        {loading ? (
          <LoadingScreen />
        ) : (
          <>
            {/* Hero Section */}
            <section className="flex items-center justify-center p-6 py-20">
              <div className="w-full max-w-7xl">
                <div className="grid lg:grid-cols-2 gap-16 items-center">
                  {/* Left side - Hero content */}
                  <div className="space-y-12">
                    <div className="space-y-8">
                      <div className="space-y-6">
                        <div className="flex items-center space-x-6">
                          <div className="relative">
                            <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-2xl animate-pulse">
                              <span className="text-white text-3xl font-bold">I</span>
                            </div>
                            <div className="absolute -inset-2 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl blur opacity-30 animate-pulse"></div>
                          </div>
                          <div>
                            <h1 className="text-5xl lg:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 leading-tight">
                              {t.hero.title}
                            </h1>
                            <p className="text-xl text-gray-400 mt-3">
                              {t.hero.subtitle}
                            </p>
                          </div>
                        </div>

                        <h2 className="text-4xl lg:text-5xl font-bold text-white leading-tight">
                          Create stunning AI-generated images in seconds
                        </h2>

                        <p className="text-xl text-gray-300 leading-relaxed max-w-2xl">
                          {t.hero.description}
                        </p>
                      </div>

                      {/* Features Grid */}
                      <div className="grid grid-cols-2 gap-6">
                        <div className="group p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 hover:scale-105">
                          <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-lg">
                              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                              </svg>
                            </div>
                            <div>
                              <h3 className="text-lg font-semibold text-white">{t.hero.unlimitedGenerations}</h3>
                              <p className="text-gray-400 text-sm">{t.hero.unlimitedGenerationsDesc}</p>
                            </div>
                          </div>
                        </div>

                        <div className="group p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 hover:scale-105">
                          <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg">
                              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                              </svg>
                            </div>
                            <div>
                              <h3 className="text-lg font-semibold text-white">{t.hero.lightningFast}</h3>
                              <p className="text-gray-400 text-sm">{t.hero.lightningFastDesc}</p>
                            </div>
                          </div>
                        </div>

                        <div className="group p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 hover:scale-105">
                          <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
                              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                              </svg>
                            </div>
                            <div>
                              <h3 className="text-lg font-semibold text-white">{t.hero.highQuality}</h3>
                              <p className="text-gray-400 text-sm">{t.hero.highQualityDesc}</p>
                            </div>
                          </div>
                        </div>

                        <div className="group p-6 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 hover:scale-105">
                          <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-pink-500 to-red-500 flex items-center justify-center shadow-lg">
                              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                              </svg>
                            </div>
                            <div>
                              <h3 className="text-lg font-semibold text-white">{t.hero.securePrivate}</h3>
                              <p className="text-gray-400 text-sm">{t.hero.securePrivateDesc}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Right side - Generation interface */}
                  <div className="relative">
                    <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-pink-500/20 rounded-3xl blur-xl"></div>
                    <div className="relative bg-black/40 backdrop-blur-xl rounded-3xl p-8 border border-white/20 shadow-2xl">
                      <div className="space-y-8">
                        <div>
                          <h3 className="text-3xl font-bold text-white mb-3">
                            {t.generator.title}
                          </h3>
                          <p className="text-gray-300 text-lg">
                            {t.generator.subtitle}
                          </p>
                        </div>

                        {/* Large text input */}
                        <div className="space-y-4">
                          <label className="block text-xl font-semibold text-white">
                            {t.generator.description}
                          </label>
                          <textarea
                            className="w-full h-40 p-6 text-lg border-2 border-white/20 rounded-2xl bg-black/30 text-white placeholder:text-gray-400 shadow-xl focus:ring-4 focus:ring-purple-500 focus:border-purple-400 focus:outline-none transition-all duration-300 resize-none backdrop-blur-sm"
                            placeholder={t.generator.descriptionPlaceholder}
                          />
                        </div>

                        {/* Style options */}
                        <div className="space-y-4">
                          <label className="block text-xl font-semibold text-white">
                            {t.generator.styleOptions}
                          </label>
                          <div className="flex flex-wrap gap-3">
                            <AspectDropdown />
                            {['No Style', 'No Color', 'No Lighting', 'No Composition'].map((label) => (
                              <button
                                key={label}
                                className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-white font-semibold shadow-lg hover:scale-105 hover:shadow-xl transition-all duration-200 border border-white/20 backdrop-blur-sm hover:bg-gradient-to-r hover:from-purple-500/30 hover:to-pink-500/30"
                              >
                                {label}
                              </button>
                            ))}
                          </div>
                        </div>

                        {/* Action buttons */}
                        <div className="flex gap-4 pt-6">
                          <button className="flex-1 px-6 py-4 rounded-xl bg-white/10 text-white font-semibold shadow-lg hover:bg-white/20 transition-all duration-200 border border-white/20 backdrop-blur-sm">
                            {t.generator.clear}
                          </button>
                          <button className="flex-1 px-6 py-4 rounded-xl bg-white/10 text-white font-semibold shadow-lg hover:bg-white/20 transition-all duration-200 border border-white/20 backdrop-blur-sm">
                            {t.generator.random}
                          </button>
                          <button className="flex-1 px-6 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-semibold shadow-xl hover:scale-105 hover:shadow-2xl transition-all duration-200 border-none focus:outline-none focus:ring-4 focus:ring-purple-400 relative overflow-hidden group">
                            <span className="relative z-10">{t.generator.generate}</span>
                            <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Sample Images Section */}
            <section className="py-20 px-6">
              <div className="max-w-7xl mx-auto">
                <div className="text-center mb-16">
                  <h2 className="text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-6">
                    {t.samples.title}
                  </h2>
                  <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                    {t.samples.subtitle}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {[
                    { title: t.samples.fantasyLandscape, prompt: t.samples.fantasyLandscapePrompt, style: "Artistic" },
                    { title: t.samples.cyberpunkCity, prompt: t.samples.cyberpunkCityPrompt, style: "Photorealistic" },
                    { title: t.samples.portraitArt, prompt: t.samples.portraitArtPrompt, style: "Classical" },
                    { title: t.samples.spaceScene, prompt: t.samples.spaceScenePrompt, style: "Sci-fi" },
                    { title: t.samples.abstractArt, prompt: t.samples.abstractArtPrompt, style: "Abstract" },
                    { title: t.samples.natureScene, prompt: t.samples.natureScenePrompt, style: "Photorealistic" }
                  ].map((image, index) => (
                    <div key={index} className="group relative">
                      <div className="aspect-square rounded-2xl overflow-hidden bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-white/20 shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-105">
                        <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                          <div className="text-center p-6">
                            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center mx-auto mb-4">
                              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                            </div>
                            <h3 className="text-lg font-semibold text-white mb-2">{image.title}</h3>
                            <p className="text-sm text-gray-400 mb-3">{image.prompt}</p>
                            <span className="inline-block px-3 py-1 rounded-full bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-300 text-xs">
                              {image.style}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-20 px-6 bg-black/20">
              <div className="max-w-7xl mx-auto">
                <div className="text-center mb-16">
                  <h2 className="text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400 mb-6">
                    {t.features.title}
                  </h2>
                  <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                    {t.features.subtitle}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {[
                    {
                      icon: "🎨",
                      title: t.features.multipleStyles,
                      description: t.features.multipleStylesDesc
                    },
                    {
                      icon: "⚡",
                      title: t.features.lightningFast,
                      description: t.features.lightningFastDesc
                    },
                    {
                      icon: "🔒",
                      title: t.features.privacyFirst,
                      description: t.features.privacyFirstDesc
                    },
                    {
                      icon: "📱",
                      title: t.features.easySharing,
                      description: t.features.easySharingDesc
                    },
                    {
                      icon: "🎯",
                      title: t.features.advancedControls,
                      description: t.features.advancedControlsDesc
                    },
                    {
                      icon: "💎",
                      title: t.features.highResolution,
                      description: t.features.highResolutionDesc
                    }
                  ].map((feature, index) => (
                    <div key={index} className="group p-8 rounded-3xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 hover:scale-105">
                      <div className="text-4xl mb-4">{feature.icon}</div>
                      <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                      <p className="text-gray-300 leading-relaxed">{feature.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* Pricing Section */}
            <section id="pricing" className="py-20 px-6">
              <div className="max-w-7xl mx-auto">
                <div className="text-center mb-16">
                  <h2 className="text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 mb-6">
                    {t.pricing.title}
                  </h2>
                  <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                    {t.pricing.subtitle}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {[
                    {
                      name: "Premium", // 修改为 Premium
                      originalName: t.pricing.free,
                      price: "$0",
                      period: t.pricing.forever,
                      features: t.pricing.features.free,
                      popular: false
                    },
                    {
                      name: "Ultimate", // 修改为 Ultimate
                      originalName: t.pricing.pro,
                      price: "$19",
                      period: t.pricing.perMonth,
                      features: t.pricing.features.pro,
                      popular: true
                    },
                    {
                      name: t.pricing.enterprise,
                      originalName: t.pricing.enterprise,
                      price: "Custom",
                      period: t.pricing.contactUs,
                      features: t.pricing.features.enterprise,
                      popular: false
                    }
                  ].map((plan, index) => (
                    <div key={index} className={`relative p-8 rounded-3xl border transition-all duration-300 hover:scale-105 ${plan.popular
                      ? 'bg-gradient-to-br from-purple-500/20 to-pink-500/20 border-purple-500/50'
                      : 'bg-white/5 border-white/10'
                      }`}>
                      {plan.popular && (
                        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                          <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-semibold">
                            {t.pricing.mostPopular}
                          </span>
                        </div>
                      )}

                      <div className="text-center">
                        <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                        <div className="mb-6">
                          <span className="text-4xl font-bold text-white">{plan.price}</span>
                          <span className="text-gray-400 ml-2">{plan.period}</span>
                        </div>

                        <ul className="space-y-4 mb-8">
                          {plan.features.map((feature, featureIndex) => (
                            <li key={featureIndex} className="flex items-center text-gray-300">
                              <svg className="w-5 h-5 text-green-400 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                              </svg>
                              {feature}
                            </li>
                          ))}
                        </ul>

                        <button 
                          onClick={() => handlePricingClick(plan.originalName)}
                          className={`w-full py-3 px-6 rounded-xl font-semibold transition-all duration-200 ${plan.popular
                            ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600'
                            : 'bg-white/10 text-white border border-white/20 hover:bg-white/20'
                            }`}>
                          {plan.originalName === t.pricing.enterprise 
                            ? t.pricing.contactSales 
                            : plan.originalName === t.pricing.free 
                              ? t.pricing.upgradingToPremium 
                              : t.pricing.upgradingToUltimate}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* FAQ Section */}
            <section className="py-20 px-6 bg-black/20">
              <div className="max-w-4xl mx-auto">
                <div className="text-center mb-16">
                  <h2 className="text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400 mb-6">
                    {t.faq.title}
                  </h2>
                  <p className="text-xl text-gray-300">
                    {t.faq.subtitle}
                  </p>
                </div>

                <div className="space-y-4">
                  {t.faq.questions.map((faq, index) => (
                    <div key={index} className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                      <button
                        className="w-full p-6 text-left flex justify-between items-center hover:bg-white/5 transition-colors duration-200"
                        onClick={() => setActiveFAQ(activeFAQ === index ? null : index)}
                      >
                        <h3 className="text-lg font-semibold text-white">{faq.question}</h3>
                        <svg
                          className={`w-6 h-6 text-gray-400 transition-transform duration-200 ${activeFAQ === index ? 'rotate-180' : ''}`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                        </svg>
                      </button>
                      {activeFAQ === index && (
                        <div className="px-6 pb-6">
                          <p className="text-gray-300 leading-relaxed">{faq.answer}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 w-full bg-black/20 backdrop-blur-xl border-t border-white/10 py-8 mt-16">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-gray-400">
            {t.footer.poweredBy} <span className="font-semibold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">Imagint Labs</span>
          </p>
        </div>
      </footer>

      {/* Sign In Modal */}
      {showSignInModal && (
        <SignInModal 
          onClose={() => setShowSignInModal(false)} 
          onLoginSuccess={() => {
            setIsLoggedIn(true);
            // 如果用户之前点击了升级按钮，现在可以继续升级流程
            if (upgradingPlan) {
              setTimeout(() => {
                window.location.href = '/dashboard';
              }, 2000);
            }
          }}
        />
      )}

      {/* Upgrading Status Modal */}
      {upgradingPlan && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-black/90 backdrop-blur-xl rounded-3xl p-8 w-full max-w-md mx-4 shadow-2xl border border-white/20">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">
                {upgradingPlan === t.pricing.free ? t.pricing.upgradingToPremium : t.pricing.upgradingToUltimate}
              </h3>
              <p className="text-gray-300 mb-6">
                Redirecting to dashboard...
              </p>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Loading Screen Component
function LoadingScreen() {
  const { t } = useLanguage();

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-12">
      <div className="relative">
        <div className="w-40 h-40 rounded-full bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-2xl animate-pulse">
          <div className="w-32 h-32 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-white text-4xl font-bold">I</span>
        </div>
        <div className="absolute -inset-4 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-full blur-xl opacity-30 animate-pulse"></div>
      </div>

      <div className="text-center space-y-6">
        <h2 className="text-4xl font-bold text-white">
          {t.loading.title}
        </h2>
        <p className="text-xl text-gray-300 animate-pulse">
          {t.loading.subtitle}<span className="animate-bounce">.</span><span className="animate-bounce delay-100">.</span><span className="animate-bounce delay-200">.</span>
        </p>
      </div>
    </div>
  );
}

// AspectDropdown Component
function AspectDropdown() {
  const { t } = useLanguage();
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState("Square Aspect");
  const ref = useRef<HTMLDivElement>(null);
  const options = ["Square Aspect", "Wide Aspect", "Tall Aspect"];

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <button
        className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-white font-semibold shadow-lg hover:scale-105 hover:shadow-xl transition-all duration-200 border border-white/20 backdrop-blur-sm hover:bg-gradient-to-r hover:from-blue-500/30 hover:to-purple-500/30 text-sm flex items-center gap-2"
        onClick={() => setOpen((v) => !v)}
      >
        {selected}
        <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="absolute left-0 mt-2 w-48 bg-black/90 backdrop-blur-xl rounded-xl shadow-2xl border border-white/20 z-20">
          {options.map((opt) => (
            <div
              key={opt}
              className={`px-4 py-3 cursor-pointer text-sm text-gray-200 hover:text-white hover:bg-white/10 transition-all duration-150 ${selected === opt ? 'font-bold bg-white/20 text-white' : ''
                }`}
              onClick={() => { setSelected(opt); setOpen(false); }}
            >
              {opt}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// SignInModal Component
function SignInModal({ onClose, onLoginSuccess }: { onClose: () => void; onLoginSuccess?: () => void }) {
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGmailSignIn = () => {
    // Gmail OAuth implementation would go here
    console.log('Gmail sign in clicked');
    // Redirect to Google OAuth endpoint
    window.location.href = API_ENDPOINTS.AUTH.GOOGLE;
  };

  const handleEmailSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post(API_ENDPOINTS.AUTH.LOGIN, {
        email,
        password
      });

      console.log('Login successful:', response.data);
      // Handle successful login (e.g., store token, redirect, etc.)
      onClose();
      if (onLoginSuccess) {
        onLoginSuccess();
      }
    } catch (err: unknown) {
      console.error('Login failed:', err);
      const errorMessage = err instanceof Error ? err.message : t.auth.error;
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-black/90 backdrop-blur-xl rounded-3xl p-8 w-full max-w-md mx-4 shadow-2xl border border-white/20">
        <div className="flex justify-between items-center mb-8">
          <h3 className="text-3xl font-bold text-white">{t.auth.signIn}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white p-2 rounded-xl hover:bg-white/10 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Gmail Sign In Button */}
        <button
          onClick={handleGmailSignIn}
          className="w-full bg-white text-gray-900 py-3 px-4 rounded-xl font-semibold transition-all duration-200 hover:bg-gray-100 flex items-center justify-center gap-3 mb-6"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
          </svg>
          {t.auth.signInWithGmail}
        </button>

        {/* Divider */}
        <div className="flex items-center mb-6">
          <div className="flex-1 border-t border-white/20"></div>
          <span className="px-4 text-gray-400 text-sm">{t.auth.or}</span>
          <div className="flex-1 border-t border-white/20"></div>
        </div>

        {/* Email/Password Form */}
        <form onSubmit={handleEmailSignIn} className="space-y-6">
          {error && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-3 text-red-300 text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-3">{t.auth.email}</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border-2 border-white/20 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-400 bg-black/30 text-white transition-colors backdrop-blur-sm"
              placeholder={t.auth.emailPlaceholder}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-3">{t.auth.password}</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border-2 border-white/20 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-400 bg-black/30 text-white transition-colors backdrop-blur-sm"
              placeholder={t.auth.passwordPlaceholder}
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-xl transition-all duration-200 font-semibold shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
          >
            {isLoading && (
              <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            )}
            {isLoading ? t.auth.loading : t.auth.signIn}
          </button>
        </form>
      </div>
    </div>
  );
}
