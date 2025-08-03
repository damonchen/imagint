declare global {
  namespace NodeJS {
    interface ProcessEnv {
      // API Configuration
      NEXT_PUBLIC_API_URL: string;
      
      // Authentication
      NEXT_PUBLIC_GOOGLE_CLIENT_ID?: string;
      NEXT_PUBLIC_GOOGLE_CLIENT_SECRET?: string;
      
      // Database
      DATABASE_URL?: string;
      
      // JWT
      JWT_SECRET?: string;
      
      // Environment
      NODE_ENV: 'development' | 'production' | 'test';
      
      // Analytics
      NEXT_PUBLIC_GA_TRACKING_ID?: string;
      
      // Feature flags
      NEXT_PUBLIC_ENABLE_ANALYTICS?: string;
      NEXT_PUBLIC_ENABLE_DEBUG_MODE?: string;
    }
  }
}

export {}; 