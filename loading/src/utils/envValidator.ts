import { env } from '../config/env';

interface ValidationResult {
    isValid: boolean;
    missingVars: string[];
    warnings: string[];
}

/**
 * Validates environment variables and returns validation result
 */
export function validateEnvironmentVariables(): ValidationResult {
    const missingVars: string[] = [];
    const warnings: string[] = [];

    // Required variables
    const requiredVars = [
        'NEXT_PUBLIC_API_URL',
    ];

    // Optional but recommended variables
    const recommendedVars = [
        'NEXT_PUBLIC_GOOGLE_CLIENT_ID',
        'NEXT_PUBLIC_GOOGLE_CLIENT_SECRET',
        'JWT_SECRET',
    ];

    // Check required variables
    requiredVars.forEach(varName => {
        if (!process.env[varName]) {
            missingVars.push(varName);
        }
    });

    // Check recommended variables
    recommendedVars.forEach(varName => {
        if (!process.env[varName]) {
            warnings.push(`${varName} is not set (optional but recommended)`);
        }
    });

    // Validate API URL format
    if (env.API_URL && !env.API_URL.startsWith('http')) {
        warnings.push('NEXT_PUBLIC_API_URL should be a valid URL starting with http:// or https://');
    }

    return {
        isValid: missingVars.length === 0,
        missingVars,
        warnings,
    };
}

/**
 * Logs environment validation results to console
 */
export function logEnvironmentValidation(): void {
    const result = validateEnvironmentVariables();

    if (!result.isValid) {
        console.info('❌ Environment validation failed:');
        console.info('Missing required environment variables:', result.missingVars);
        console.info('Please check your .env.local file');
    } else {
        console.log('✅ Environment validation passed');
    }

    if (result.warnings.length > 0) {
        console.warn('⚠️ Environment warnings:');
        result.warnings.forEach(warning => console.warn(`  - ${warning}`));
    }
}

/**
 * Throws an error if required environment variables are missing
 */
export function assertEnvironmentVariables(): void {
    const result = validateEnvironmentVariables();

    if (!result.isValid) {
        throw new Error(
            `Missing required environment variables: ${result.missingVars.join(', ')}. ` +
            'Please check your .env.local file and ensure all required variables are set.'
        );
    }
} 