// Environment variables configuration
export const env = {
  // API Configuration
  API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://192.168.187.144:3000',

  // Authentication
  GOOGLE_CLIENT_ID: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '',
  GOOGLE_CLIENT_SECRET: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_SECRET || '',

  // Database
  DATABASE_URL: process.env.DATABASE_URL || '',

  // JWT
  JWT_SECRET: process.env.JWT_SECRET || '',

  // Environment
  NODE_ENV: process.env.NODE_ENV || 'development',
  IS_PRODUCTION: process.env.NODE_ENV === 'production',
  IS_DEVELOPMENT: process.env.NODE_ENV === 'development',

  // Analytics
  GA_TRACKING_ID: process.env.NEXT_PUBLIC_GA_TRACKING_ID || '',

  // Feature flags
  ENABLE_ANALYTICS: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
  ENABLE_DEBUG_MODE: process.env.NEXT_PUBLIC_ENABLE_DEBUG_MODE === 'true',
} as const;

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: `${env.API_URL}/api/v1/auth/login`,
    GOOGLE: `${env.API_URL}/api/v1/auth/google`,
    LOGOUT: `${env.API_URL}/api/v1/auth/logout`,
    REGISTER: `${env.API_URL}/api/v1/auth/register`,
  },
  USER: {
    PROFILE: `${env.API_URL}/api/v1/user/profile`,
    UPDATE: `${env.API_URL}/api/v1/user/update`,
  },
} as const;

// Validation function to check required environment variables
export function validateEnvironment() {
  const requiredVars = [
    'NEXT_PUBLIC_API_URL',
  ];

  const missingVars = requiredVars.filter(varName => !process.env[varName]);

  if (missingVars.length > 0) {
    console.warn('Missing required environment variables:', missingVars);
  }

  return missingVars.length === 0;
} 