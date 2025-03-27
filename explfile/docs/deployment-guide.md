# VoxStitch Deployment Guide

## Prerequisites

1. **System Requirements**
   - Node.js 16+
   - Python 3.9+
   - Redis 6+
   - PostgreSQL 13+
   - AWS Account (for S3)

2. **Environment Setup**
   ```bash
   # Clone repository
   git clone https://github.com/your-org/voxstitch.git
   cd voxstitch
   
   # Install dependencies
   # Frontend
   cd frontend
   npm install
   
   # Backend
   cd ../backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

## Configuration

### 1. Environment Variables

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
REACT_APP_GITHUB_CLIENT_ID=your_github_client_id
REACT_APP_APPLE_CLIENT_ID=your_apple_client_id
```

#### Backend (.env)
```env
# Server
PORT=8000
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,https://voxstitch.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/voxstitch

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-west-2
MEDIA_BUCKET=voxstitch-media

# OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:3000/auth/github/callback

APPLE_CLIENT_ID=your_apple_client_id
APPLE_TEAM_ID=your_apple_team_id
APPLE_KEY_ID=your_apple_key_id
APPLE_PRIVATE_KEY=your_apple_private_key
APPLE_REDIRECT_URI=http://localhost:3000/auth/apple/callback

# OpenAI
OPENAI_API_KEY=your_openai_api_key
```

### 2. Database Setup
```sql
-- Create database
CREATE DATABASE voxstitch;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### 3. AWS S3 Setup
1. Create S3 bucket
2. Configure CORS:
```json
{
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST"],
            "AllowedOrigins": ["http://localhost:3000", "https://voxstitch.com"],
            "ExposeHeaders": ["ETag"]
        }
    ]
}
```

## Development Deployment

1. **Start Backend**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

2. **Start Frontend**
```bash
cd frontend
npm start
```

## Production Deployment

### 1. Backend Deployment (Using Docker)

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: voxstitch
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 2. Frontend Deployment

1. Build frontend:
```bash
cd frontend
npm run build
```

2. Configure web server (Nginx):
```nginx
server {
    listen 80;
    server_name voxstitch.com;

    location / {
        root /var/www/voxstitch;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL Configuration (Let's Encrypt)
```bash
certbot --nginx -d voxstitch.com
```

## Monitoring & Maintenance

### 1. Logging
- Use CloudWatch for AWS services
- Set up ELK stack for application logs
- Monitor Redis with Redis Insights

### 2. Backup Strategy
```bash
# Database backup
pg_dump voxstitch > backup.sql

# Redis backup
redis-cli save

# S3 backup (using AWS CLI)
aws s3 sync s3://voxstitch-media backup/
```

### 3. Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

## Security Checklist

1. **SSL/TLS**
   - Enable HTTPS
   - Configure SSL certificates
   - Set up HSTS

2. **Authentication**
   - Secure JWT configuration
   - Rate limiting
   - CSRF protection

3. **Data Protection**
   - Database encryption
   - Secure file uploads
   - Regular security updates

## Scaling Considerations

1. **Load Balancing**
   - Use AWS ELB or Nginx
   - Configure session affinity
   - Set up health checks

2. **Database Scaling**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **Caching Strategy**
   - Redis cluster
   - CDN for static assets
   - Response caching

## Troubleshooting

### Common Issues

1. **Database Connections**
```bash
# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql-13-main.log

# Check connections
psql -U user -d voxstitch -c "SELECT count(*) FROM pg_stat_activity;"
```

2. **Redis Issues**
```bash
# Monitor Redis
redis-cli monitor

# Check memory usage
redis-cli info memory
```

3. **Application Errors**
```bash
# Check application logs
tail -f /var/log/voxstitch/app.log

# Check nginx logs
tail -f /var/log/nginx/error.log
```

## Rollback Procedure

1. **Database Rollback**
```bash
# Restore from backup
psql voxstitch < backup.sql
```

2. **Application Rollback**
```bash
# Using Docker
docker-compose down
git checkout previous-version
docker-compose up -d
```

3. **Frontend Rollback**
```bash
# Revert to previous build
mv /var/www/voxstitch/backup /var/www/voxstitch/current
nginx -s reload
```
