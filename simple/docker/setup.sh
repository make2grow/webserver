#!/bin/bash
# setup.sh - Setup script for the project

echo "🚀 Setting up Multi-Subdomain Docker Project..."
echo "==============================================="

# Make scripts executable
chmod +x test.sh

echo "✅ Made scripts executable"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Show project structure
echo ""
echo "📁 Project Structure:"
find . -type f -name "*.py" -o -name "*.yml" -o -name "*.conf" -o -name "Dockerfile" | sort

echo ""
echo "📝 Next Steps:"
echo "1. Add DNS entries to /etc/hosts:"
echo "   sudo echo '127.0.0.1 app1.example.com' >> /etc/hosts"
echo "   sudo echo '127.0.0.1 api.example.com' >> /etc/hosts"
echo "   sudo echo '127.0.0.1 admin.example.com' >> /etc/hosts"
echo ""
echo "2. Start the services:"
echo "   docker-compose up -d --build"
echo ""
echo "3. Test the setup:"
echo "   ./test.sh"
echo ""
echo "4. Visit the applications:"
echo "   - Frontend: http://app1.example.com"
echo "   - API: http://api.example.com"
echo "   - Admin: http://admin.example.com"

echo ""
echo "✅ Setup completed!"