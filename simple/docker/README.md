# Multi-Subdomain Docker Web Applications

This project demonstrates how to run multiple web applications on different subdomains using Docker and Nginx reverse proxy.

## Project Structure

```
docker/
├── docker-compose.yml          # Main orchestration file
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf              # Reverse proxy configuration
├── app1/                       # Frontend Application
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── app2/                       # API Server
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── app3/                       # Admin Panel
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── README.md
└── test.sh                     # Test script
```

## Applications

1. **App 1 - Frontend** (app1.example.com:80 → container:3000)
   - Simulates a React/Vue.js frontend application
   - Colorful gradient background
   - Test endpoints: `/api/status`, `/api/data`

2. **App 2 - API Server** (api.example.com:80 → container:8000)
   - REST API with user management
   - Endpoints: `/api/users`, `/api/stats`
   - JSON responses for testing

3. **App 3 - Admin Panel** (admin.example.com:80 → container:5000)
   - Admin dashboard with system metrics
   - Endpoints: `/admin/logs`, `/admin/users`, `/admin/settings`

## Quick Start

### 1. Setup DNS (Local Development)

Add these entries to your `/etc/hosts` file:

```
127.0.0.1 app1.example.com
127.0.0.1 api.example.com
127.0.0.1 admin.example.com
```

### 2. Test Individual Apps (Optional)

Before using Docker, you can test individual applications:

```bash
# Install Flask
pip install Flask psutil

# Test App 1
cd app1 && python app.py
# Visit: http://localhost:3000

# Test App 2 (new terminal)
cd app2 && python app.py
# Visit: http://localhost:8000

# Test App 3 (new terminal)
cd app3 && python app.py
# Visit: http://localhost:5000
```

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Test the Setup

Visit these URLs in your browser:
- http://app1.example.com - Frontend Application
- http://api.example.com - API Server
- http://admin.example.com - Admin Panel

Or run the test script:
```bash
chmod +x test.sh
./test.sh
```

## API Endpoints

### App 1 (Frontend)
- `GET /` - Homepage with server info
- `GET /api/status` - Service status
- `GET /api/data` - Sample data
- `GET /health` - Health check

### App 2 (API Server)
- `GET /` - API documentation
- `GET /api/users` - Get all users
- `POST /api/users` - Create user
- `GET /api/stats` - Server statistics
- `GET /health` - Health check

### App 3 (Admin Panel)
- `GET /` - Admin dashboard
- `GET /admin/logs` - System logs
- `GET /admin/users` - User management
- `GET /admin/settings` - System settings
- `GET /health` - Health check

## Docker Commands

```bash
# Start services
docker-compose up -d

# Build specific service
docker-compose build app1

# Restart specific service
docker-compose restart app1

# View logs for specific service
docker-compose logs -f app1

# Execute command in running container
docker-compose exec app1 /bin/bash

# Scale a service (if needed)
docker-compose up -d --scale app1=3

# Remove everything
docker-compose down -v --remove-orphans
```

## Troubleshooting

### Problem: "Bad Gateway" error
- Check if application containers are running: `docker-compose ps`
- Check application logs: `docker-compose logs app1`
- Verify nginx configuration

### Problem: DNS not resolving
- Check `/etc/hosts` entries for local development
- For production: verify DNS A records point to your server IP

### Problem: Port conflicts
- Make sure ports 80 and 443 are not used by other services
- Stop other web servers (Apache, other nginx instances)

### Problem: Container won't start
- Check Docker logs: `docker-compose logs [service-name]`
- Verify Dockerfile and requirements.txt syntax
- Check available disk space and memory

## Production Deployment

For production deployment:

1. **Update DNS records** to point to your server IP
2. **Add SSL certificates** (Let's Encrypt recommended)
3. **Update docker-compose.yml** for production settings
4. **Use environment variables** for sensitive configuration
5. **Set up log rotation** and monitoring

## Architecture

```
Internet → Nginx (Port 80/443) → Docker Network → Flask Apps (3000/8000/5000)
          ↓
    Subdomain Routing:
    - app1.example.com → app1:3000
    - api.example.com  → app2:8000  
    - admin.example.com → app3:5000
```

This setup provides:
- ✅ Simple subdomain routing
- ✅ Containerized applications
- ✅ Easy scaling and maintenance
- ✅ Health monitoring
- ✅ Production-ready foundation