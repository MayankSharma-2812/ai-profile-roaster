# 🔥 AI Profile Roaster - Quick Reference

## 📖 Files You Need to Know

| File                      | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| `config.py`               | Environment-based configuration (dev/prod) |
| `.env.example`            | Template for environment variables         |
| `.env`                    | Your local secrets (⚠️ never commit)       |
| `Procfile`                | Heroku deployment configuration            |
| `Dockerfile`              | Container image definition                 |
| `docker-compose.yml`      | Local Docker development                   |
| `wsgi.py`                 | WSGI entry point for production            |
| `setup.sh`                | One-command setup script                   |
| `DEPLOYMENT.md`           | Full deployment guide                      |
| `DEPLOYMENT_CHECKLIST.md` | Pre-deployment checklist                   |

---

## 🚀 Running the App

### Development

```bash
python -m web.app
# Opens on http://localhost:8500
```

### Production (Local Testing)

```bash
gunicorn -b 0.0.0.0:8500 web.app:app
```

### Docker

```bash
docker-compose up
# OR
docker build -t ai-roaster . && docker run -p 8500:8500 -e OPENAI_API_KEY=sk-... ai-roaster
```

---

## 🔧 Configuration

### Development Config

```python
FLASK_ENV=development
DEBUG=True
SESSION_COOKIE_SECURE=False
```

### Production Config

```python
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<random-32-char-key>
SESSION_COOKIE_SECURE=True
```

### Set via environment:

```bash
export OPENAI_API_KEY=sk-...
export FLASK_ENV=production
export SECRET_KEY=$(openssl rand -base64 32)
```

---

## 📦 Dependencies

### Core

- `Flask` - Web framework
- `openai` - OpenAI API client
- `spacy` - NLP library
- `pdfplumber` - PDF parsing

### Production Server

- `gunicorn` - WSGI server
- `python-dotenv` - Environment management

### Optional

- `groq` - Groq API (free alternative to OpenAI)

Manage with:

```bash
pip install -r requirements.txt      # Development
pip install -r requirements-prod.txt # Production
```

---

## 🜔 Security Checklist

Before production:

- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` has no real credentials
- [ ] `SECRET_KEY` is set to random value (not "dev-key")
- [ ] `FLASK_ENV=production` is set
- [ ] API keys are in environment variables, not code
- [ ] HTTPS is enabled
- [ ] Monitoring is configured

---

## 📊 API Endpoints

| Method | Endpoint   | Input        | Output        |
| ------ | ---------- | ------------ | ------------- |
| GET    | `/`        | -            | HTML homepage |
| POST   | `/analyze` | text or file | HTML or JSON  |

### POST /analyze

```bash
curl -X POST http://localhost:8500/analyze \
  -F "text=Your profile text..."

# OR upload file
curl -X POST http://localhost:8500/analyze \
  -F "file=@resume.pdf"
```

---

## 🐛 Debugging

### Check imports

```bash
python -c "from web.app import app; print('✓ OK')"
```

### Test API key

```bash
echo $OPENAI_API_KEY
# Should output: sk-...
```

### View logs

```bash
# Docker
docker-compose logs -f web

# Systemd service
journalctl -u ai-roaster -f

# Gunicorn
gunicorn --access-logfile - --error-logfile - web.app:app
```

### Port issues

```bash
# Find process on port 8500
lsof -i :8500

# Kill it
kill -9 <PID>
```

---

## 🚢 Deployment Quick Links

| Platform   | Guide               | Setup Time |
| ---------- | ------------------- | ---------- |
| **Local**  | `python -m web.app` | 2 min      |
| **Docker** | `docker-compose up` | 3 min      |
| **Heroku** | See `DEPLOYMENT.md` | 5 min      |
| **Server** | See `DEPLOYMENT.md` | 15 min     |

---

## 📞 Troubleshooting

**"No module named roaster"**

```bash
# Run from project root
cd /home/miku/ai-profile-roaster
python -m web.app
```

**"API key invalid"**

```bash
# Check it's set
echo $OPENAI_API_KEY

# Try Groq instead
export GROQ_API_KEY=gsk-...
```

**"Port 8500 in use"**

```bash
# Change port
export PORT=8501
python -m web.app

# Or kill the process
lsof -i :8500 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

For more help, read:

- `DEPLOYMENT.md` - Full guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-launch checklist
- `README.md` - Features & setup

---

## 🎯 Common Tasks

### Add new feature

1. Edit relevant file in `roaster/` or `web/`
2. Test locally: `python -m web.app`
3. Build Docker image: `docker build -t ai-roaster .`
4. Deploy via Docker or Heroku

### Update dependencies

```bash
# Add to requirements.txt or requirements-prod.txt
pip install new-package
pip freeze > requirements.txt

# Or specify version
pip install new-package==1.0.0
```

### Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# OR
openssl rand -base64 32
```

### Test production build locally

```bash
docker build -t ai-roaster .
docker run -p 8500:8500 \
  -e OPENAI_API_KEY=sk-... \
  -e FLASK_ENV=production \
  -e SECRET_KEY=... \
  ai-roaster
```

---

## 📚 More Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Groq API Docs](https://console.groq.com/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Docker Docs](https://docs.docker.com/)

---

## 🆘 Need Help?

1. Check `DEPLOYMENT.md` for detailed guides
2. Review `DEPLOYMENT_CHECKLIST.md` before launch
3. Check logs: `docker-compose logs` or `journalctl`
4. Verify environment variables: `env | grep -i openai`
5. Test imports: `python -c "from web.app import app"`

**Everything is configured. You're ready to deploy! 🚀**
