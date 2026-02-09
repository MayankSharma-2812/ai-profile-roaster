# Deployment Guide 🚀

## Pre-deployment Checklist

- [ ] Remove all test files and backup files
- [ ] Update `.env.example` with all required variables
- [ ] Set up production API keys (OpenAI or Groq)
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Run security audit
- [ ] Test with `config.ProductionConfig`

## Local Development Setup

```bash
# Clone repository
git clone <your-repo-url>
cd ai-profile-roaster

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
# Edit .env with your API keys

# (Optional) Download spaCy model for better NLP
python -m spacy download en_core_web_sm

# Run development server
python -m web.app
```

Visit `http://localhost:8500` in your browser.

## Production Deployment

### Option 1: Heroku Deployment

```bash
# Install Heroku CLI (if not already installed)
curl https://cli.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-your-key-here
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secure-random-key

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy app
COPY . .

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Expose port
EXPOSE 8500

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8500/ || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8500", "--workers", "4", "--timeout", "120", "web.app:app"]
```

Build and run:

```bash
docker build -t ai-roaster .
docker run -p 8500:8500 -e OPENAI_API_KEY=sk-... ai-roaster
```

### Option 3: Traditional Server (Ubuntu/Debian)

```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone <your-repo-url>
cd ai-profile-roaster

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-prod.txt

# Create .env file with production keys
nano .env
# Add: OPENAI_API_KEY=sk-...
# Add: FLASK_ENV=production
# Add: SECRET_KEY=<generate-random-key>

# Test with gunicorn
gunicorn --bind 0.0.0.0:8500 --workers 4 web.app:app
```

Create systemd service file `/etc/systemd/system/ai-roaster.service`:

```ini
[Unit]
Description=AI Profile Roaster
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ai-profile-roaster
Environment="PATH=/var/www/ai-profile-roaster/venv/bin"
ExecStart=/var/www/ai-profile-roaster/venv/bin/gunicorn \
    --bind 0.0.0.0:8500 \
    --workers 4 \
    --timeout 120 \
    web.app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-roaster
sudo systemctl start ai-roaster
sudo systemctl status ai-roaster
```

Set up Nginx reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8500;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10M;
    }

    location /static {
        alias /var/www/ai-profile-roaster/web/static;
        expires 30d;
    }
}
```

Enable SSL with Let's Encrypt:

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Environment Variables

| Variable          | Required   | Default    | Description                          |
| ----------------- | ---------- | ---------- | ------------------------------------ |
| `OPENAI_API_KEY`  | Optional   | -          | OpenAI API key for AI roasts         |
| `GROQ_API_KEY`    | Optional   | -          | Groq API key (free alternative)      |
| `FLASK_ENV`       | No         | production | Environment (production/development) |
| `SECRET_KEY`      | Yes (Prod) | dev-key    | Session secret key                   |
| `PORT`            | No         | 8500       | Server port                          |
| `HOST`            | No         | 0.0.0.0    | Server host                          |
| `MAX_UPLOAD_SIZE` | No         | 10485760   | Max file upload (bytes)              |

## Security Recommendations

✅ **Done:**

- Config-based environment management
- `.env` excluded from git
- `.env.example` template provided
- Production WSGI server (gunicorn)
- Secure session cookies
- Input validation via Flask

✅ **Recommended for Full Production:**

- Add rate limiting (Flask-Limiter)
- Add request size limits
- Use PostgreSQL for sessions
- Enable HTTPS/SSL
- Add API authentication
- Implement logging/monitoring
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)

## Performance Tips

1. **Use gunicorn workers**: 4-8 workers for CPU-bound tasks
2. **Enable caching**: Add HTTP caching headers for static files
3. **Database**: Use PostgreSQL for session management if scaling
4. **CDN**: Serve static files from CloudFront or similar
5. **Monitoring**: Add error tracking (Sentry) and performance monitoring

## Troubleshooting

**Port already in use:**

```bash
# Find process using port 8500
lsof -i :8500
# Kill it
kill -9 <PID>
```

**Permission denied:**

```bash
# On systemd service, ensure user has access:
sudo chown -R www-data:www-data /var/www/ai-profile-roaster
```

**API key not loading:**

```bash
# Check environment
echo $OPENAI_API_KEY
# Reload service
sudo systemctl reload ai-roaster
```

## Monitoring & Maintenance

```bash
# Check service status
sudo systemctl status ai-roaster

# View recent logs
sudo journalctl -u ai-roaster -n 50

# Restart service
sudo systemctl restart ai-roaster

# Monitor disk/CPU
htop
```

## Support

For issues or questions:

1. Check logs: `sudo journalctl -u ai-roaster`
2. Test locally first: `python -m web.app`
3. Verify API keys: `echo $OPENAI_API_KEY`
4. Open an issue on GitHub
