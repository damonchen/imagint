# Environment Variables Configuration

This document describes all the environment variables used in this project and how to configure them.

## Quick Setup

1. Run the setup script:
   ```bash
   npm run setup
   ```

2. Edit `.env.local` and update the values according to your setup.

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Your API server URL | `http://localhost:3000` |

### Optional Variables

#### Authentication
| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | Google OAuth client ID | `123456789-abcdef.apps.googleusercontent.com` |
| `NEXT_PUBLIC_GOOGLE_CLIENT_SECRET` | Google OAuth client secret | `your_secret_here` |
| `JWT_SECRET` | Secret key for JWT tokens | `your_jwt_secret_here` |

#### Database
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@localhost:5432/db` |

#### Analytics
| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_GA_TRACKING_ID` | Google Analytics tracking ID | `G-XXXXXXXXXX` |

#### Feature Flags
| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | Enable analytics tracking | `false` |
| `NEXT_PUBLIC_ENABLE_DEBUG_MODE` | Enable debug mode | `true` |

## Environment Files

- `.env.local` - Local development environment (not committed to git)
- `.env.production` - Production environment
- `.env.example` - Example configuration file

## Usage in Code

### Import Environment Configuration

```typescript
import { env, API_ENDPOINTS } from '../config/env';

// Use environment variables
const apiUrl = env.API_URL;
const isProduction = env.IS_PRODUCTION;

// Use API endpoints
const loginUrl = API_ENDPOINTS.AUTH.LOGIN;
```

### Validate Environment Variables

```typescript
import { logEnvironmentValidation, assertEnvironmentVariables } from '../utils/envValidator';

// Log validation results
logEnvironmentValidation();

// Throw error if required variables are missing
assertEnvironmentVariables();
```

## Security Notes

1. **Never commit sensitive environment variables** to version control
2. **Use `NEXT_PUBLIC_` prefix** only for variables that need to be accessible in the browser
3. **Server-side variables** (like `JWT_SECRET`) should not have the `NEXT_PUBLIC_` prefix
4. **Use strong, unique secrets** for production environments

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Check that `.env.local` exists and contains the required variables
   - Ensure variable names are spelled correctly

2. **"API calls failing"**
   - Verify `NEXT_PUBLIC_API_URL` is set correctly
   - Check that the API server is running

3. **"Google OAuth not working"**
   - Ensure `NEXT_PUBLIC_GOOGLE_CLIENT_ID` is set
   - Verify the client ID is correct and the OAuth app is configured properly

### Validation

The application automatically validates environment variables on startup. Check the browser console for validation messages.

## Production Deployment

For production deployment:

1. Set all required environment variables in your hosting platform
2. Use strong, unique secrets for production
3. Ensure `NODE_ENV=production` is set
4. Configure proper CORS settings for your API URL 