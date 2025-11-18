#!/bin/bash

# Hostinger Deployment Script for SectionduWeb
# Run this script on your Hostinger server after uploading files

echo "========================================="
echo "SectionduWeb - Hostinger Deployment"
echo "========================================="
echo ""

# Get project directory
PROJECT_DIR="$HOME/public_html/videovote"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Are you in the project directory?"
    echo "Please cd to your project directory and run this script again."
    exit 1
fi

echo "✅ Found project files"
echo ""

# Step 1: Check Python version
echo "1. Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1)
echo "   $PYTHON_VERSION"
echo ""

# Step 2: Create necessary directories
echo "2. Creating necessary directories..."
mkdir -p static/uploads
mkdir -p static/avatars
mkdir -p static/thumbnails
mkdir -p logs
mkdir -p tmp
echo "   ✅ Directories created"
echo ""

# Step 3: Set permissions
echo "3. Setting correct permissions..."
chmod 755 .
chmod 644 app.py
chmod 644 config.py
chmod 644 passenger_wsgi.py
chmod 644 .htaccess
chmod 600 .env 2>/dev/null || echo "   ⚠️  .env file not found"
chmod 755 static
chmod 755 static/uploads
chmod 755 static/avatars
chmod 755 static/thumbnails
chmod 755 templates
chmod 755 logs
chmod 755 tmp
echo "   ✅ Permissions set"
echo ""

# Step 4: Check if .env exists
echo "4. Checking environment configuration..."
if [ -f ".env" ]; then
    echo "   ✅ .env file found"
else
    echo "   ⚠️  .env file not found!"
    echo "   Creating template .env file..."
    cat > .env << 'EOF'
# Flask Configuration
SECRET_KEY=your_super_secret_key_change_this_in_production
FLASK_ENV=production

# Database
DATABASE_URL=sqlite:///tournament.db

# Cloud Storage
USE_CLOUD_STORAGE=true

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=videovote-uploads
AWS_REGION=us-east-1

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Mobile Money Configuration
MTN_MOMO_API_USER=
MTN_MOMO_API_KEY=
MTN_MOMO_SUBSCRIPTION_KEY=

# Demo Mode
DEMO_MODE=false
EOF
    chmod 600 .env
    echo "   ⚠️  Please edit .env file with your actual credentials!"
fi
echo ""

# Step 5: Install Python dependencies
echo "5. Installing Python dependencies..."
if pip3 install --user -r requirements.txt; then
    echo "   ✅ Dependencies installed successfully"
else
    echo "   ❌ Error installing dependencies"
    echo "   Try: pip3 install --user -r requirements.txt"
    exit 1
fi
echo ""

# Step 6: Initialize database
echo "6. Initializing database..."
if [ -f "tournament.db" ]; then
    echo "   ⚠️  Database already exists, skipping initialization"
else
    python3 -c "from app import init_db; init_db()" 2>/dev/null
    if [ -f "tournament.db" ]; then
        echo "   ✅ Database initialized"
        chmod 644 tournament.db
    else
        echo "   ⚠️  Database initialization may have failed"
        echo "   The app will create it on first run"
    fi
fi
echo ""

# Step 7: Test imports
echo "7. Testing Python imports..."
if python3 -c "import flask, werkzeug, boto3, cloudinary; print('✅ All main packages imported successfully')" 2>/dev/null; then
    echo "   ✅ Import test passed"
else
    echo "   ⚠️  Some imports failed, but application might still work"
fi
echo ""

# Step 8: Create restart file
echo "8. Creating restart trigger..."
touch tmp/restart.txt
echo "   ✅ Application will restart"
echo ""

# Step 9: Check S3 configuration
echo "9. Checking S3 configuration..."
if python3 -c "from s3_storage import s3_storage; print('Available:', s3_storage.is_available())" 2>/dev/null; then
    echo "   ✅ S3 configuration checked"
else
    echo "   ⚠️  S3 check failed (this is OK if not using S3)"
fi
echo ""

# Step 10: Display summary
echo "========================================="
echo "Deployment Summary"
echo "========================================="
echo ""
echo "✅ Project directory: $PROJECT_DIR"
echo "✅ Permissions set correctly"
echo "✅ Dependencies installed"
echo "✅ Database initialized (if new)"
echo ""
echo "⚠️  Important Next Steps:"
echo "1. Edit .env file with your actual credentials"
echo "2. Configure Python app in hPanel"
echo "3. Set up SSL certificate"
echo "4. Point domain/subdomain to this directory"
echo "5. Test your application"
echo ""
echo "📝 To restart application later:"
echo "   touch $PROJECT_DIR/tmp/restart.txt"
echo ""
echo "📝 View logs:"
echo "   tail -f $HOME/logs/error.log"
echo ""
echo "🚀 Deployment script completed!"
echo "========================================="
