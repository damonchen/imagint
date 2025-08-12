export type Language = 'en' | 'zh' | 'ar' | 'es' | 'pt';

export interface Translations {
    nav: {
        features: string;
        pricing: string;
        about: string;
        signIn: string;
    };
    hero: {
        title: string;
        subtitle: string;
        description: string;
        unlimitedGenerations: string;
        unlimitedGenerationsDesc: string;
        lightningFast: string;
        lightningFastDesc: string;
        highQuality: string;
        highQualityDesc: string;
        securePrivate: string;
        securePrivateDesc: string;
    };
    generator: {
        title: string;
        subtitle: string;
        description: string;
        descriptionPlaceholder: string;
        styleOptions: string;
        clear: string;
        random: string;
        generate: string;
    };
    auth: {
        signIn: string;
        email: string;
        password: string;
        emailPlaceholder: string;
        passwordPlaceholder: string;
        signInWithGmail: string;
        or: string;
        loading: string;
        error: string;
    };
    samples: {
        title: string;
        subtitle: string;
        fantasyLandscape: string;
        fantasyLandscapePrompt: string;
        cyberpunkCity: string;
        cyberpunkCityPrompt: string;
        portraitArt: string;
        portraitArtPrompt: string;
        spaceScene: string;
        spaceScenePrompt: string;
        abstractArt: string;
        abstractArtPrompt: string;
        natureScene: string;
        natureScenePrompt: string;
    };
    features: {
        title: string;
        subtitle: string;
        multipleStyles: string;
        multipleStylesDesc: string;
        lightningFast: string;
        lightningFastDesc: string;
        privacyFirst: string;
        privacyFirstDesc: string;
        easySharing: string;
        easySharingDesc: string;
        advancedControls: string;
        advancedControlsDesc: string;
        highResolution: string;
        highResolutionDesc: string;
    };
    pricing: {
        title: string;
        subtitle: string;
        free: string;
        pro: string;
        enterprise: string;
        forever: string;
        perMonth: string;
        contactUs: string;
        mostPopular: string;
        getStarted: string;
        contactSales: string;
        upgradingToPremium: string;
        upgradingToUltimate: string;
        pleaseSignIn: string;
        features: {
            free: string[];
            pro: string[];
            enterprise: string[];
        };
    };
    faq: {
        title: string;
        subtitle: string;
        questions: Array<{
            question: string;
            answer: string;
        }>;
    };
    footer: {
        poweredBy: string;
    };
    loading: {
        title: string;
        subtitle: string;
    };
}

export const translations: Record<Language, Translations> = {
    en: {
        nav: {
            features: "Features",
            pricing: "Pricing",
            about: "About",
            signIn: "Sign In"
        },
        hero: {
            title: "Imagint AI",
            subtitle: "World's First Unlimited Free AI Image Generator",
            description: "Transform your ideas into beautiful artwork with our advanced AI technology. No limits, no restrictions, completely free.",
            unlimitedGenerations: "Unlimited Generations",
            unlimitedGenerationsDesc: "No restrictions on usage",
            lightningFast: "Lightning Fast",
            lightningFastDesc: "Generate in seconds",
            highQuality: "High Quality",
            highQualityDesc: "4K resolution output",
            securePrivate: "Secure & Private",
            securePrivateDesc: "Your data is protected"
        },
        generator: {
            title: "Create Your Image",
            subtitle: "Describe what you want to see and watch the magic happen",
            description: "Description",
            descriptionPlaceholder: "Describe your perfect image... e.g., 'A majestic dragon flying over a sunset mountain landscape with vibrant colors'",
            styleOptions: "Style Options",
            clear: "Clear",
            random: "Random",
            generate: "Generate"
        },
        auth: {
            signIn: "Sign In",
            email: "Email",
            password: "Password",
            emailPlaceholder: "Enter your email",
            passwordPlaceholder: "Enter your password",
            signInWithGmail: "Sign in with Gmail",
            or: "or",
            loading: "Signing in...",
            error: "Invalid email or password"
        },
        samples: {
            title: "See What Our AI Can Create",
            subtitle: "Explore stunning examples of AI-generated images created by our users",
            fantasyLandscape: "Fantasy Landscape",
            fantasyLandscapePrompt: "A mystical forest with glowing mushrooms and floating islands",
            cyberpunkCity: "Cyberpunk City",
            cyberpunkCityPrompt: "Neon-lit futuristic cityscape with flying cars",
            portraitArt: "Portrait Art",
            portraitArtPrompt: "Elegant woman in renaissance style portrait",
            spaceScene: "Space Scene",
            spaceScenePrompt: "Galaxy with colorful nebulas and distant planets",
            abstractArt: "Abstract Art",
            abstractArtPrompt: "Colorful geometric patterns with flowing gradients",
            natureScene: "Nature Scene",
            natureScenePrompt: "Serene mountain lake at golden hour"
        },
        features: {
            title: "Powerful Features",
            subtitle: "Everything you need to create stunning AI-generated images",
            multipleStyles: "Multiple Styles",
            multipleStylesDesc: "Choose from photorealistic, artistic, cartoon, anime, and many more styles to match your vision.",
            lightningFast: "Lightning Fast",
            lightningFastDesc: "Generate high-quality images in seconds with our optimized AI processing pipeline.",
            privacyFirst: "Privacy First",
            privacyFirstDesc: "Your prompts and generated images are encrypted and never shared without your permission.",
            easySharing: "Easy Sharing",
            easySharingDesc: "Share your creations instantly on social media or download them directly to your device.",
            advancedControls: "Advanced Controls",
            advancedControlsDesc: "Fine-tune your images with aspect ratios, style modifiers, and detailed prompts.",
            highResolution: "High Resolution",
            highResolutionDesc: "Generate images up to 4K resolution for professional use and printing."
        },
        pricing: {
            title: "Choose Your Plan",
            subtitle: "Start free and upgrade when you need more power",
            free: "Free",
            pro: "Pro",
            enterprise: "Enterprise",
            forever: "forever",
            perMonth: "per month",
            contactUs: "contact us",
            mostPopular: "Most Popular",
            getStarted: "Get Started",
            contactSales: "Contact Sales",
            upgradingToPremium: "Upgrading to Premium",
            upgradingToUltimate: "Upgrading to Ultimate",
            pleaseSignIn: "Please sign in to continue",
            features: {
                free: [
                    "50 images per day",
                    "1024x1024 resolution",
                    "Basic styles",
                    "Community support",
                    "Standard processing"
                ],
                pro: [
                    "Unlimited images",
                    "4096x4096 resolution",
                    "All styles & models",
                    "Priority support",
                    "Advanced editing tools",
                    "Commercial license"
                ],
                enterprise: [
                    "Custom model training",
                    "API access",
                    "Dedicated support",
                    "White-label solution",
                    "Custom integrations",
                    "SLA guarantee"
                ]
            }
        },
        faq: {
            title: "Frequently Asked Questions",
            subtitle: "Everything you need to know about Imagint AI",
            questions: [
                {
                    question: "What is Imagint AI?",
                    answer: "Imagint AI is a cutting-edge AI image generation platform that allows you to create stunning, unique images from text descriptions completely free of charge."
                },
                {
                    question: "Is it really free?",
                    answer: "Yes! We offer unlimited free image generation. While we have premium features available, our core service remains free for everyone."
                },
                {
                    question: "How do I get started?",
                    answer: "Simply sign up for a free user, enter your text prompt describing the image you want, and let our AI do the magic!"
                },
                {
                    question: "What image styles are available?",
                    answer: "We support various styles including photorealistic, artistic, cartoon, anime, and many more. You can specify your preferred style in the prompt."
                },
                {
                    question: "Can I use the generated images commercially?",
                    answer: "Yes, all images generated with Imagint AI come with a commercial license. You own full rights to your creations."
                },
                {
                    question: "What's the image resolution?",
                    answer: "Free users can generate images up to 1024x1024 pixels. Premium users get access to higher resolutions up to 4096x4096."
                }
            ]
        },
        footer: {
            poweredBy: "Powered by"
        },
        loading: {
            title: "Preparing Your AI Experience",
            subtitle: "Loading amazing features"
        }
    },
    zh: {
        nav: {
            features: "功能",
            pricing: "定价",
            about: "关于",
            signIn: "登录"
        },
        hero: {
            title: "Imagint AI",
            subtitle: "全球首个无限免费AI图像生成器",
            description: "使用我们先进的AI技术将您的想法转化为精美艺术品。无限制，无约束，完全免费。",
            unlimitedGenerations: "无限生成",
            unlimitedGenerationsDesc: "无使用限制",
            lightningFast: "闪电速度",
            lightningFastDesc: "秒级生成",
            highQuality: "高质量",
            highQualityDesc: "4K分辨率输出",
            securePrivate: "安全私密",
            securePrivateDesc: "您的数据受保护"
        },
        generator: {
            title: "创建您的图像",
            subtitle: "描述您想要看到的内容，见证魔法发生",
            description: "描述",
            descriptionPlaceholder: "描述您完美的图像...例如：'一只雄伟的龙在日落山景中飞翔，色彩鲜艳'",
            styleOptions: "风格选项",
            clear: "清除",
            random: "随机",
            generate: "生成"
        },
        auth: {
            signIn: "登录",
            email: "邮箱",
            password: "密码",
            emailPlaceholder: "输入您的邮箱",
            passwordPlaceholder: "输入您的密码",
            signInWithGmail: "使用Gmail登录",
            or: "或",
            loading: "登录中...",
            error: "邮箱或密码错误"
        },
        samples: {
            title: "看看我们的AI能创造什么",
            subtitle: "探索我们用户创建的令人惊叹的AI生成图像示例",
            fantasyLandscape: "奇幻风景",
            fantasyLandscapePrompt: "一个神秘的森林，有发光的蘑菇和漂浮的岛屿",
            cyberpunkCity: "赛博朋克城市",
            cyberpunkCityPrompt: "霓虹灯照明的未来城市景观，有飞行汽车",
            portraitArt: "肖像艺术",
            portraitArtPrompt: "文艺复兴风格的优雅女性肖像",
            spaceScene: "太空场景",
            spaceScenePrompt: "有彩色星云和遥远行星的星系",
            abstractArt: "抽象艺术",
            abstractArtPrompt: "彩色几何图案，流动的渐变",
            natureScene: "自然场景",
            natureScenePrompt: "黄金时分的宁静山湖"
        },
        features: {
            title: "强大功能",
            subtitle: "创建令人惊叹的AI生成图像所需的一切",
            multipleStyles: "多种风格",
            multipleStylesDesc: "选择写实、艺术、卡通、动漫等多种风格来匹配您的愿景。",
            lightningFast: "闪电速度",
            lightningFastDesc: "通过我们优化的AI处理管道在几秒钟内生成高质量图像。",
            privacyFirst: "隐私优先",
            privacyFirstDesc: "您的提示词和生成的图像都经过加密，未经您的许可绝不共享。",
            easySharing: "轻松分享",
            easySharingDesc: "立即在社交媒体上分享您的创作或直接下载到您的设备。",
            advancedControls: "高级控制",
            advancedControlsDesc: "通过宽高比、风格修饰符和详细提示词来微调您的图像。",
            highResolution: "高分辨率",
            highResolutionDesc: "生成高达4K分辨率的图像，适用于专业用途和打印。"
        },
        pricing: {
            title: "选择您的计划",
            subtitle: "免费开始，需要更多功能时升级",
            free: "免费",
            pro: "专业版",
            enterprise: "企业版",
            forever: "永久",
            perMonth: "每月",
            contactUs: "联系我们",
            mostPopular: "最受欢迎",
            getStarted: "开始使用",
            contactSales: "联系销售",
            upgradingToPremium: "升级到高级版",
            upgradingToUltimate: "升级到终极版",
            pleaseSignIn: "请登录以继续",
            features: {
                free: [
                    "每天50张图像",
                    "1024x1024分辨率",
                    "基础风格",
                    "社区支持",
                    "标准处理"
                ],
                pro: [
                    "无限图像",
                    "4096x4096分辨率",
                    "所有风格和模型",
                    "优先支持",
                    "高级编辑工具",
                    "商业许可"
                ],
                enterprise: [
                    "自定义模型训练",
                    "API访问",
                    "专属支持",
                    "白标解决方案",
                    "自定义集成",
                    "SLA保证"
                ]
            }
        },
        faq: {
            title: "常见问题",
            subtitle: "关于Imagint AI您需要了解的一切",
            questions: [
                {
                    question: "什么是Imagint AI？",
                    answer: "Imagint AI是一个尖端的AI图像生成平台，允许您从文本描述创建令人惊叹的独特图像，完全免费。"
                },
                {
                    question: "真的免费吗？",
                    answer: "是的！我们提供无限免费图像生成。虽然我们有高级功能可用，但我们的核心服务对所有人保持免费。"
                },
                {
                    question: "如何开始使用？",
                    answer: "只需注册一个免费账户，输入描述您想要图像的文本提示，让我们的AI施展魔法！"
                },
                {
                    question: "有哪些图像风格可用？",
                    answer: "我们支持各种风格，包括写实、艺术、卡通、动漫等。您可以在提示中指定您喜欢的风格。"
                },
                {
                    question: "我可以商业使用生成的图像吗？",
                    answer: "是的，所有使用Imagint AI生成的图像都带有商业许可。您拥有创作的全部权利。"
                },
                {
                    question: "图像分辨率是多少？",
                    answer: "免费用户最多可生成1024x1024像素的图像。高级用户可获得高达4096x4096的更高分辨率。"
                }
            ]
        },
        footer: {
            poweredBy: "由以下公司提供技术支持"
        },
        loading: {
            title: "准备您的AI体验",
            subtitle: "加载精彩功能"
        }
    },
    ar: {
        nav: {
            features: "الميزات",
            pricing: "الأسعار",
            about: "حول",
            signIn: "تسجيل الدخول"
        },
        hero: {
            title: "Imagint AI",
            subtitle: "أول مولد صور ذكي مجاني غير محدود في العالم",
            description: "حول أفكارك إلى أعمال فنية جميلة باستخدام تقنية الذكاء الاصطناعي المتقدمة لدينا. بلا حدود، بلا قيود، مجاني تماماً.",
            unlimitedGenerations: "توليد غير محدود",
            unlimitedGenerationsDesc: "لا توجد قيود على الاستخدام",
            lightningFast: "سريع كالبرق",
            lightningFastDesc: "توليد في ثوانٍ",
            highQuality: "جودة عالية",
            highQualityDesc: "دقة 4K",
            securePrivate: "آمن وخاص",
            securePrivateDesc: "بياناتك محمية"
        },
        generator: {
            title: "أنشئ صورتك",
            subtitle: "صف ما تريد رؤيته وشاهد السحر يحدث",
            description: "الوصف",
            descriptionPlaceholder: "صف صورتك المثالية... مثال: 'تنين مهيب يطير فوق منظر جبلي عند غروب الشمس بألوان نابضة بالحياة'",
            styleOptions: "خيارات النمط",
            clear: "مسح",
            random: "عشوائي",
            generate: "توليد"
        },
        auth: {
            signIn: "تسجيل الدخول",
            email: "البريد الإلكتروني",
            password: "كلمة المرور",
            emailPlaceholder: "أدخل بريدك الإلكتروني",
            passwordPlaceholder: "أدخل كلمة المرور",
            signInWithGmail: "تسجيل الدخول بـ Gmail",
            or: "أو",
            loading: "جاري تسجيل الدخول...",
            error: "البريد الإلكتروني أو كلمة المرور غير صحيحة"
        },
        samples: {
            title: "شاهد ما يمكن لذكائنا الاصطناعي إنشاؤه",
            subtitle: "استكشف أمثلة مذهلة للصور المولدة بالذكاء الاصطناعي التي أنشأها مستخدمونا",
            fantasyLandscape: "منظر خيالي",
            fantasyLandscapePrompt: "غابة غامضة مع فطر متوهج وجزر عائمة",
            cyberpunkCity: "مدينة سايبربانك",
            cyberpunkCityPrompt: "منظر مدينة مستقبلية مضاءة بالنيون مع سيارات طائرة",
            portraitArt: "فن البورتريه",
            portraitArtPrompt: "امرأة أنيقة بورتريه بأسلوب عصر النهضة",
            spaceScene: "مشهد فضائي",
            spaceScenePrompt: "مجرة مع سحب ملونة وكواكب بعيدة",
            abstractArt: "فن تجريدي",
            abstractArtPrompt: "أنماط هندسية ملونة مع تدرجات متدفقة",
            natureScene: "مشهد طبيعي",
            natureScenePrompt: "بحيرة جبلية هادئة في الساعة الذهبية"
        },
        features: {
            title: "ميزات قوية",
            subtitle: "كل ما تحتاجه لإنشاء صور مذهلة مولدة بالذكاء الاصطناعي",
            multipleStyles: "أنماط متعددة",
            multipleStylesDesc: "اختر من بين أنماط واقعية وفنية وكرتونية وأنيمي وغيرها الكثير لتناسب رؤيتك.",
            lightningFast: "سريع كالبرق",
            lightningFastDesc: "توليد صور عالية الجودة في ثوانٍ مع خط معالجة الذكاء الاصطناعي المحسن لدينا.",
            privacyFirst: "الخصوصية أولاً",
            privacyFirstDesc: "نصوصك والصور المولدة مشفرة ولا تُشارك أبداً بدون إذنك.",
            easySharing: "مشاركة سهلة",
            easySharingDesc: "شارك إبداعاتك فوراً على وسائل التواصل الاجتماعي أو حملها مباشرة إلى جهازك.",
            advancedControls: "تحكم متقدم",
            advancedControlsDesc: "ضبط صورك بدقة مع نسب الأبعاد ومواد النمط والنصوص التفصيلية.",
            highResolution: "دقة عالية",
            highResolutionDesc: "توليد صور بدقة تصل إلى 4K للاستخدام المهني والطباعة."
        },
        pricing: {
            title: "اختر خطتك",
            subtitle: "ابدأ مجاناً وارتقِ عندما تحتاج المزيد من القوة",
            free: "مجاني",
            pro: "احترافي",
            enterprise: "المؤسسات",
            forever: "للأبد",
            perMonth: "شهرياً",
            contactUs: "اتصل بنا",
            mostPopular: "الأكثر شعبية",
            getStarted: "ابدأ الآن",
            contactSales: "اتصل بالمبيعات",
            upgradingToPremium: "الترقية إلى المميز",
            upgradingToUltimate: "الترقية إلى النهائي",
            pleaseSignIn: "يرجى تسجيل الدخول للمتابعة",
            features: {
                free: [
                    "50 صورة يومياً",
                    "دقة 1024x1024",
                    "أنماط أساسية",
                    "دعم المجتمع",
                    "معالجة قياسية"
                ],
                pro: [
                    "صور غير محدودة",
                    "دقة 4096x4096",
                    "جميع الأنماط والنماذج",
                    "دعم ذو أولوية",
                    "أدوات تحرير متقدمة",
                    "ترخيص تجاري"
                ],
                enterprise: [
                    "تدريب نموذج مخصص",
                    "وصول API",
                    "دعم مخصص",
                    "حل علامة بيضاء",
                    "تكامل مخصص",
                    "ضمان SLA"
                ]
            }
        },
        faq: {
            title: "الأسئلة الشائعة",
            subtitle: "كل ما تحتاج معرفته عن Imagint AI",
            questions: [
                {
                    question: "ما هو Imagint AI؟",
                    answer: "Imagint AI هو منصة توليد صور ذكية متطورة تسمح لك بإنشاء صور فريدة مذهلة من الأوصاف النصية مجاناً تماماً."
                },
                {
                    question: "هل هو مجاني حقاً؟",
                    answer: "نعم! نقدم توليد صور مجاني غير محدود. بينما لدينا ميزات متقدمة متاحة، خدمتنا الأساسية تبقى مجانية للجميع."
                },
                {
                    question: "كيف أبدأ؟",
                    answer: "ببساطة سجل حساب مجاني، أدخل النص الوصفي للصورة التي تريدها، ودع ذكائنا الاصطناعي يفعل السحر!"
                },
                {
                    question: "ما الأنماط المتاحة؟",
                    answer: "ندعم أنماطاً مختلفة تشمل الواقعية والفنية والكرتونية والأنيمي وغيرها الكثير. يمكنك تحديد النمط المفضل في النص."
                },
                {
                    question: "هل يمكنني استخدام الصور تجارياً؟",
                    answer: "نعم، جميع الصور المولدة بـ Imagint AI تأتي مع ترخيص تجاري. أنت تملك حقوق إبداعاتك بالكامل."
                },
                {
                    question: "ما دقة الصور؟",
                    answer: "يمكن للمستخدمين المجانيين توليد صور حتى 1024x1024 بكسل. المستخدمون المتقدمون يحصلون على دقة أعلى تصل إلى 4096x4096."
                }
            ]
        },
        footer: {
            poweredBy: "مدعوم بواسطة"
        },
        loading: {
            title: "تحضير تجربة الذكاء الاصطناعي",
            subtitle: "تحميل ميزات مذهلة"
        }
    },
    es: {
        nav: {
            features: "Características",
            pricing: "Precios",
            about: "Acerca de",
            signIn: "Iniciar Sesión"
        },
        hero: {
            title: "Imagint AI",
            subtitle: "El Primer Generador de Imágenes IA Gratuito e Ilimitado del Mundo",
            description: "Transforma tus ideas en hermosas obras de arte con nuestra tecnología IA avanzada. Sin límites, sin restricciones, completamente gratis.",
            unlimitedGenerations: "Generaciones Ilimitadas",
            unlimitedGenerationsDesc: "Sin restricciones de uso",
            lightningFast: "Velocidad Relámpago",
            lightningFastDesc: "Genera en segundos",
            highQuality: "Alta Calidad",
            highQualityDesc: "Resolución 4K",
            securePrivate: "Seguro y Privado",
            securePrivateDesc: "Tus datos están protegidos"
        },
        generator: {
            title: "Crea Tu Imagen",
            subtitle: "Describe lo que quieres ver y observa la magia suceder",
            description: "Descripción",
            descriptionPlaceholder: "Describe tu imagen perfecta... ej: 'Un dragón majestuoso volando sobre un paisaje montañoso al atardecer con colores vibrantes'",
            styleOptions: "Opciones de Estilo",
            clear: "Limpiar",
            random: "Aleatorio",
            generate: "Generar"
        },
        auth: {
            signIn: "Iniciar Sesión",
            email: "Correo Electrónico",
            password: "Contraseña",
            emailPlaceholder: "Ingresa tu correo electrónico",
            passwordPlaceholder: "Ingresa tu contraseña",
            signInWithGmail: "Iniciar sesión con Gmail",
            or: "o",
            loading: "Iniciando sesión...",
            error: "Correo electrónico o contraseña inválidos"
        },
        samples: {
            title: "Mira Lo Que Nuestra IA Puede Crear",
            subtitle: "Explora ejemplos impresionantes de imágenes generadas por IA creadas por nuestros usuarios",
            fantasyLandscape: "Paisaje Fantástico",
            fantasyLandscapePrompt: "Un bosque místico con hongos brillantes e islas flotantes",
            cyberpunkCity: "Ciudad Cyberpunk",
            cyberpunkCityPrompt: "Paisaje urbano futurista iluminado con neón con coches voladores",
            portraitArt: "Arte de Retrato",
            portraitArtPrompt: "Mujer elegante retrato en estilo renacentista",
            spaceScene: "Escena Espacial",
            spaceScenePrompt: "Galaxia con nebulosas coloridas y planetas distantes",
            abstractArt: "Arte Abstracto",
            abstractArtPrompt: "Patrones geométricos coloridos con gradientes fluidos",
            natureScene: "Escena Natural",
            natureScenePrompt: "Lago de montaña sereno en la hora dorada"
        },
        features: {
            title: "Características Potentes",
            subtitle: "Todo lo que necesitas para crear imágenes impresionantes generadas por IA",
            multipleStyles: "Múltiples Estilos",
            multipleStylesDesc: "Elige entre estilos fotorrealistas, artísticos, caricatura, anime y muchos más para que coincidan con tu visión.",
            lightningFast: "Velocidad Relámpago",
            lightningFastDesc: "Genera imágenes de alta calidad en segundos con nuestro pipeline de procesamiento IA optimizado.",
            privacyFirst: "Privacidad Primero",
            privacyFirstDesc: "Tus prompts e imágenes generadas están encriptadas y nunca se comparten sin tu permiso.",
            easySharing: "Compartir Fácil",
            easySharingDesc: "Comparte tus creaciones instantáneamente en redes sociales o descárgalas directamente a tu dispositivo.",
            advancedControls: "Controles Avanzados",
            advancedControlsDesc: "Ajusta tus imágenes con proporciones de aspecto, modificadores de estilo y prompts detallados.",
            highResolution: "Alta Resolución",
            highResolutionDesc: "Genera imágenes de hasta 4K de resolución para uso profesional e impresión."
        },
        pricing: {
            title: "Elige Tu Plan",
            subtitle: "Comienza gratis y actualiza cuando necesites más poder",
            free: "Gratis",
            pro: "Pro",
            enterprise: "Empresa",
            forever: "para siempre",
            perMonth: "por mes",
            contactUs: "contáctanos",
            mostPopular: "Más Popular",
            getStarted: "Comenzar",
            contactSales: "Contactar Ventas",
            upgradingToPremium: "Actualizando a Premium",
            upgradingToUltimate: "Actualizando a Ultimate",
            pleaseSignIn: "Por favor inicia sesión para continuar",
            features: {
                free: [
                    "50 imágenes por día",
                    "Resolución 1024x1024",
                    "Estilos básicos",
                    "Soporte comunitario",
                    "Procesamiento estándar"
                ],
                pro: [
                    "Imágenes ilimitadas",
                    "Resolución 4096x4096",
                    "Todos los estilos y modelos",
                    "Soporte prioritario",
                    "Herramientas de edición avanzadas",
                    "Licencia comercial"
                ],
                enterprise: [
                    "Entrenamiento de modelo personalizado",
                    "Acceso API",
                    "Soporte dedicado",
                    "Solución white-label",
                    "Integraciones personalizadas",
                    "Garantía SLA"
                ]
            }
        },
        faq: {
            title: "Preguntas Frecuentes",
            subtitle: "Todo lo que necesitas saber sobre Imagint AI",
            questions: [
                {
                    question: "¿Qué es Imagint AI?",
                    answer: "Imagint AI es una plataforma de generación de imágenes IA de vanguardia que te permite crear imágenes únicas e impresionantes a partir de descripciones de texto completamente gratis."
                },
                {
                    question: "¿Es realmente gratis?",
                    answer: "¡Sí! Ofrecemos generación de imágenes gratuita ilimitada. Aunque tenemos características premium disponibles, nuestro servicio básico permanece gratis para todos."
                },
                {
                    question: "¿Cómo empiezo?",
                    answer: "¡Simplemente regístrate para una cuenta gratuita, ingresa tu prompt de texto describiendo la imagen que quieres, y deja que nuestra IA haga la magia!"
                },
                {
                    question: "¿Qué estilos de imagen están disponibles?",
                    answer: "Soportamos varios estilos incluyendo fotorrealista, artístico, caricatura, anime y muchos más. Puedes especificar tu estilo preferido en el prompt."
                },
                {
                    question: "¿Puedo usar las imágenes generadas comercialmente?",
                    answer: "Sí, todas las imágenes generadas con Imagint AI vienen con una licencia comercial. Eres dueño de todos los derechos de tus creaciones."
                },
                {
                    question: "¿Cuál es la resolución de imagen?",
                    answer: "Los usuarios gratuitos pueden generar imágenes de hasta 1024x1024 píxeles. Los usuarios premium obtienen acceso a resoluciones más altas de hasta 4096x4096."
                }
            ]
        },
        footer: {
            poweredBy: "Desarrollado por"
        },
        loading: {
            title: "Preparando Tu Experiencia IA",
            subtitle: "Cargando características increíbles"
        }
    },
    pt: {
        nav: {
            features: "Recursos",
            pricing: "Preços",
            about: "Sobre",
            signIn: "Entrar"
        },
        hero: {
            title: "Imagint AI",
            subtitle: "O Primeiro Gerador de Imagens IA Gratuito e Ilimitado do Mundo",
            description: "Transforme suas ideias em belas obras de arte com nossa tecnologia IA avançada. Sem limites, sem restrições, completamente grátis.",
            unlimitedGenerations: "Gerações Ilimitadas",
            unlimitedGenerationsDesc: "Sem restrições de uso",
            lightningFast: "Velocidade Relâmpago",
            lightningFastDesc: "Gere em segundos",
            highQuality: "Alta Qualidade",
            highQualityDesc: "Resolução 4K",
            securePrivate: "Seguro e Privado",
            securePrivateDesc: "Seus dados estão protegidos"
        },
        generator: {
            title: "Crie Sua Imagem",
            subtitle: "Descreva o que você quer ver e observe a mágica acontecer",
            description: "Descrição",
            descriptionPlaceholder: "Descreva sua imagem perfeita... ex: 'Um dragão majestoso voando sobre uma paisagem montanhosa ao pôr do sol com cores vibrantes'",
            styleOptions: "Opções de Estilo",
            clear: "Limpar",
            random: "Aleatório",
            generate: "Gerar"
        },
        auth: {
            signIn: "Entrar",
            email: "E-mail",
            password: "Senha",
            emailPlaceholder: "Digite seu e-mail",
            passwordPlaceholder: "Digite sua senha",
            signInWithGmail: "Entrar com Gmail",
            or: "ou",
            loading: "Entrando...",
            error: "E-mail ou senha inválidos"
        },
        samples: {
            title: "Veja O Que Nossa IA Pode Criar",
            subtitle: "Explore exemplos impressionantes de imagens geradas por IA criadas por nossos usuários",
            fantasyLandscape: "Paisagem Fantástica",
            fantasyLandscapePrompt: "Uma floresta mística com cogumelos brilhantes e ilhas flutuantes",
            cyberpunkCity: "Cidade Cyberpunk",
            cyberpunkCityPrompt: "Paisagem urbana futurista iluminada com néon com carros voadores",
            portraitArt: "Arte de Retrato",
            portraitArtPrompt: "Mulher elegante retrato em estilo renascentista",
            spaceScene: "Cena Espacial",
            spaceScenePrompt: "Galáxia com nebulosas coloridas e planetas distantes",
            abstractArt: "Arte Abstrata",
            abstractArtPrompt: "Padrões geométricos coloridos com gradientes fluidos",
            natureScene: "Cena Natural",
            natureScenePrompt: "Lago de montanha sereno na hora dourada"
        },
        features: {
            title: "Recursos Poderosos",
            subtitle: "Tudo que você precisa para criar imagens impressionantes geradas por IA",
            multipleStyles: "Múltiplos Estilos",
            multipleStylesDesc: "Escolha entre estilos fotorrealistas, artísticos, cartoon, anime e muitos mais para combinar com sua visão.",
            lightningFast: "Velocidade Relâmpago",
            lightningFastDesc: "Gere imagens de alta qualidade em segundos com nosso pipeline de processamento IA otimizado.",
            privacyFirst: "Privacidade Primeiro",
            privacyFirstDesc: "Seus prompts e imagens geradas são criptografados e nunca são compartilhados sem sua permissão.",
            easySharing: "Compartilhamento Fácil",
            easySharingDesc: "Compartilhe suas criações instantaneamente nas redes sociais ou baixe-as diretamente para seu dispositivo.",
            advancedControls: "Controles Avançados",
            advancedControlsDesc: "Ajuste suas imagens com proporções de aspecto, modificadores de estilo e prompts detalhados.",
            highResolution: "Alta Resolução",
            highResolutionDesc: "Gere imagens de até 4K de resolução para uso profissional e impressão."
        },
        pricing: {
            title: "Escolha Seu Plano",
            subtitle: "Comece grátis e atualize quando precisar de mais poder",
            free: "Grátis",
            pro: "Pro",
            enterprise: "Empresa",
            forever: "para sempre",
            perMonth: "por mês",
            contactUs: "entre em contato",
            mostPopular: "Mais Popular",
            getStarted: "Começar",
            contactSales: "Contatar Vendas",
            upgradingToPremium: "Atualizando para Premium",
            upgradingToUltimate: "Atualizando para Ultimate",
            pleaseSignIn: "Por favor, faça login para continuar",
            features: {
                free: [
                    "50 imagens por dia",
                    "Resolução 1024x1024",
                    "Estilos básicos",
                    "Suporte da comunidade",
                    "Processamento padrão"
                ],
                pro: [
                    "Imagens ilimitadas",
                    "Resolução 4096x4096",
                    "Todos os estilos e modelos",
                    "Suporte prioritário",
                    "Ferramentas de edição avançadas",
                    "Licença comercial"
                ],
                enterprise: [
                    "Treinamento de modelo personalizado",
                    "Acesso API",
                    "Suporte dedicado",
                    "Solução white-label",
                    "Integrações personalizadas",
                    "Garantia SLA"
                ]
            }
        },
        faq: {
            title: "Perguntas Frequentes",
            subtitle: "Tudo que você precisa saber sobre Imagint AI",
            questions: [
                {
                    question: "O que é Imagint AI?",
                    answer: "Imagint AI é uma plataforma de geração de imagens IA de ponta que permite criar imagens únicas e impressionantes a partir de descrições de texto completamente grátis."
                },
                {
                    question: "É realmente grátis?",
                    answer: "Sim! Oferecemos geração de imagens gratuita ilimitada. Embora tenhamos recursos premium disponíveis, nosso serviço básico permanece grátis para todos."
                },
                {
                    question: "Como começo?",
                    answer: "Simplesmente registre-se para uma conta gratuita, digite seu prompt de texto descrevendo a imagem que você quer, e deixe nossa IA fazer a mágica!"
                },
                {
                    question: "Quais estilos de imagem estão disponíveis?",
                    answer: "Suportamos vários estilos incluindo fotorrealista, artístico, cartoon, anime e muitos mais. Você pode especificar seu estilo preferido no prompt."
                },
                {
                    question: "Posso usar as imagens geradas comercialmente?",
                    answer: "Sim, todas as imagens geradas com Imagint AI vêm com uma licença comercial. Você possui todos os direitos de suas criações."
                },
                {
                    question: "Qual é a resolução da imagem?",
                    answer: "Usuários gratuitos podem gerar imagens de até 1024x1024 pixels. Usuários premium obtêm acesso a resoluções mais altas de até 4096x4096."
                }
            ]
        },
        footer: {
            poweredBy: "Desenvolvido por"
        },
        loading: {
            title: "Preparando Sua Experiência IA",
            subtitle: "Carregando recursos incríveis"
        }
    }
}; 