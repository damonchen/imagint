#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up environment variables...\n');

const envExamplePath = path.join(__dirname, '..', 'env.example');
const envLocalPath = path.join(__dirname, '..', '.env.local');

// Check if .env.local already exists
if (fs.existsSync(envLocalPath)) {
  console.log('⚠️  .env.local already exists. Skipping...');
  console.log('   If you want to reset it, delete .env.local and run this script again.\n');
} else {
  // Check if env.example exists
  if (!fs.existsSync(envExamplePath)) {
    console.error('❌ env.example file not found!');
    process.exit(1);
  }

  // Copy env.example to .env.local
  try {
    fs.copyFileSync(envExamplePath, envLocalPath);
    console.log('✅ Created .env.local from env.example');
    console.log('📝 Please update the values in .env.local according to your setup\n');
  } catch (error) {
    console.error('❌ Failed to create .env.local:', error.message);
    process.exit(1);
  }
}

// Display next steps
console.log('📋 Next steps:');
console.log('1. Edit .env.local and update the values');
console.log('2. Run "npm run dev" to start the development server');
console.log('3. Open http://localhost:3000 in your browser\n');

console.log('🔧 Required environment variables:');
console.log('   - NEXT_PUBLIC_API_URL: Your API server URL');
console.log('   - NEXT_PUBLIC_GOOGLE_CLIENT_ID: Google OAuth client ID (optional)');
console.log('   - NEXT_PUBLIC_GOOGLE_CLIENT_SECRET: Google OAuth client secret (optional)');
console.log('   - JWT_SECRET: Secret key for JWT tokens (optional)');
console.log('   - DATABASE_URL: Database connection string (optional)\n');

console.log('💡 Tip: Check the README.md file for more detailed setup instructions.'); 