#!/bin/bash
# test.sh - Test script for subdomain setup

echo "🧪 Testing Multi-Subdomain Docker Setup..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test if Docker is running
echo -e "${BLUE}Checking Docker status...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker is running${NC}"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml not found. Make sure you're in the correct directory.${NC}"
    exit 1
fi

# Check /etc/hosts for local DNS entries
echo -e "${BLUE}Checking /etc/hosts entries...${NC}"
if grep -q "app1.example.com" /etc/hosts && grep -q "api.example.com" /etc/hosts && grep -q "admin.example.com" /etc/hosts; then
    echo -e "${GREEN}✅ DNS entries found in /etc/hosts${NC}"
else
    echo -e "${YELLOW}⚠️ DNS entries missing. Add these to /etc/hosts:${NC}"
    echo "127.0.0.1 app1.example.com"
    echo "127.0.0.1 api.example.com"
    echo "127.0.0.1 admin.example.com"
    echo ""
fi

# Start services if not running
echo -e "${BLUE}Checking container status...${NC}"
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Starting services...${NC}"
    docker-compose up -d --build
    echo -e "${YELLOW}Waiting 30 seconds for services to start...${NC}"
    sleep 30
fi

# Check container status
echo -e "${BLUE}Container Status:${NC}"
docker-compose ps

echo ""
echo -e "${BLUE}Testing Health Endpoints...${NC}"

# Test health endpoints
services=("app1:3000" "app2:8000" "app3:5000")
for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    echo -n "Testing $name ($port): "
    if curl -s -f http://localhost:$port/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Healthy${NC}"
    else
        echo -e "${RED}❌ Not responding${NC}"
    fi
done

echo ""
echo -e "${BLUE}Testing Subdomain Routing...${NC}"

# Test subdomain routing
subdomains=("app1.example.com" "api.example.com" "admin.example.com")
for subdomain in "${subdomains[@]}"; do
    echo -n "Testing $subdomain: "
    status_code=$(curl -s -o /dev/null -w "%{http_code}" "http://$subdomain/" 2>/dev/null)
    if [ "$status_code" = "200" ]; then
        echo -e "${GREEN}✅ HTTP $status_code${NC}"
    else
        echo -e "${RED}❌ HTTP $status_code${NC}"
    fi
done

echo ""
echo -e "${BLUE}Testing API Endpoints...${NC}"

# Test specific API endpoints
echo -n "Frontend status: "
response=$(curl -s "http://app1.example.com/api/status" 2>/dev/null | grep -o '"status":"[^"]*"' 2>/dev/null)
if [ -n "$response" ]; then
    echo -e "${GREEN}✅ $response${NC}"
else
    echo -e "${RED}❌ No response${NC}"
fi

echo -n "API users: "
response=$(curl -s "http://api.example.com/api/users" 2>/dev/null | grep -o '"total":[0-9]*' 2>/dev/null)
if [ -n "$response" ]; then
    echo -e "${GREEN}✅ $response${NC}"
else
    echo -e "${RED}❌ No response${NC}"
fi

echo -n "Admin logs: "
response=$(curl -s "http://admin.example.com/admin/logs" 2>/dev/null | grep -o '"total":[0-9]*' 2>/dev/null)
if [ -n "$response" ]; then
    echo -e "${GREEN}✅ $response${NC}"
else
    echo -e "${RED}❌ No response${NC}"
fi

echo ""
echo -e "${BLUE}Docker Network Information:${NC}"
docker network ls | grep docker

echo ""
echo -e "${BLUE}Resource Usage:${NC}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
echo -e "${YELLOW}🔧 Useful Commands:${NC}"
echo "• View logs: docker-compose logs -f"
echo "• Restart services: docker-compose restart"
echo "• Stop everything: docker-compose down"
echo "• Rebuild: docker-compose up -d --build"
echo "• Shell access: docker-compose exec app1 /bin/bash"

echo ""
echo -e "${YELLOW}📱 Test URLs:${NC}"
echo "• Frontend: http://app1.example.com"
echo "• API: http://api.example.com"
echo "• Admin: http://admin.example.com"

echo ""
if docker-compose ps | grep -q "Up.*healthy"; then
    echo -e "${GREEN}🎉 All services are running and healthy!${NC}"
else
    echo -e "${YELLOW}⚠️ Some services may need attention. Check logs with: docker-compose logs${NC}"
fi

echo -e "${BLUE}✅ Test completed!${NC}"