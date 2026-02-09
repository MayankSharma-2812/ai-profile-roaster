# AI Profile Roaster 🔥

A brutal AI-powered profile/resume roaster that generates custom, savage roasts and actionable improvement suggestions.

## Features

- **AI-Powered Roasts**: Uses OpenAI's GPT to generate custom, brutal roasts based on your actual profile text (not templated)
- **Smart Analysis**: Detects clichés, missing metrics, skills mentioned, and more
- **Actionable Suggestions**: Get AI-driven improvement tips specific to your profile
- **CLI & Web UI**: Use via terminal or web interface
- **PDF Support**: Analyze PDF resumes directly

## Setup

### 1. Clone/Open the Project

```bash
cd /home/miku/ai-profile-roaster
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root using the template:

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:

```bash
OPENAI_API_KEY=sk-your-key-here
GROQ_API_KEY=gsk-your-groq-key-here  # Optional: Free alternative to OpenAI
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

**⚠️ SECURITY**: Never commit `.env` to git. The file is automatically excluded.

### 5. (Optional) Install spaCy Model for Better NLP

```bash
python -m spacy download en_core_web_sm
```

## Usage

### Web UI (Recommended)

```bash
python -m web.app
```

Open http://localhost:8500 in your browser.

### Command Line

```bash
python -m roaster.main resume.txt
# or with a PDF
python -m roaster.main resume.pdf
```

## How It Works

1. **Parse**: Extracts text from `.txt` or `.pdf` files
2. **Analyze**: Detects profiles, clichés, skills, metrics, and sentence structure
3. **AI Roast**: Sends to OpenAI to generate custom brutal roasts
4. **Fallback**: If API is unavailable, uses predefined roasts
5. **Suggestions**: AI generates actionable improvement tips

## Example Input

```
I am a passionate and hardworking developer.
I am a fast learner and team player.
I know Python and Java.
I improved test coverage by 30%.
```

## Example AI Roast

```
Your profile reads like every other junior dev's LinkedIn headline. "Passionate"? "Team player"?
Recruiters sleep through these phrases weekly.

You buried a real achievement (30% test coverage) under three sentences of buzzwords. Lead with metrics.

"I know Python and Java" — okay, but what did you *build*?
```

## API Endpoints

### GET `/`

Returns the web UI homepage.

### POST `/analyze`

Analyzes a profile. Accepts:

- `text` (form): Profile text to analyze
- `file` (form): `.txt` or `.pdf` file to upload

Returns HTML or JSON (if `Accept: application/json` or `?json=1`).

## Without OpenAI API

The app gracefully falls back to predefined roasts if:

- `OPENAI_API_KEY` is not set
- The API is unavailable
- API call fails

Predefined roasts are still useful but not custom to your profile.

## Environment Variables

| Variable         | Required | Description                                                                  |
| ---------------- | -------- | ---------------------------------------------------------------------------- |
| `OPENAI_API_KEY` | Optional | OpenAI API key for custom AI roasts. Without it, predefined roasts are used. |
| `GROQ_API_KEY`   | Optional | Groq API key (free tier). Used if OpenAI not available.                      |
| `FLASK_ENV`      | No       | `development` or `production` (default: `production`)                        |
| `SECRET_KEY`     | Yes\*    | Secret key for sessions. Required in production.                             |
| `PORT`           | No       | Server port (default: `8500`)                                                |
| `HOST`           | No       | Server host (default: `0.0.0.0`)                                             |

\*Required only in production mode.

## Troubleshooting

**"No module named 'roaster'"**

- Run from project root: `python -m web.app` (not `python web/app.py`)
- Or set `PYTHONPATH=.` before running

**API Key errors**

- Verify `OPENAI_API_KEY` is set: `echo $OPENAI_API_KEY`
- Check your key is valid at https://platform.openai.com/account/api-keys
- Try Groq API as a free alternative

**Port 8500 already in use**

- Change the port in `.env`: `PORT=8501`
- Or kill existing process: `lsof -i :8500 && kill -9 <PID>`

## Deployment

### Quick Start with Docker

```bash
docker build -t ai-roaster .
docker run -p 8500:8500 -e OPENAI_API_KEY=sk-... ai-roaster
```

### Heroku Deployment

```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

### Production Server Deployment

See [**DEPLOYMENT.md**](DEPLOYMENT.md) for complete deployment guide:

- Heroku setup
- Docker containerization
- Traditional server (Ubuntu/Debian)
- Nginx reverse proxy configuration
- Security best practices
- Performance optimization

## Project Structure

```
.
├── roaster/
│   ├── main.py           # CLI entry point
│   ├── parser.py         # Text/PDF extraction
│   ├── analyzer.py       # Profile analysis
│   ├── roast_engine.py   # Predefined roasts
│   ├── suggestions.py    # Predefined suggestions
│   ├── ai_roaster.py     # AI-powered roasts & suggestions
├── web/
│   ├── app.py            # Flask web server
│   ├── templates/
│   │   └── index.html    # Web UI
│   └── static/
│       └── style.css     # Styling
├── requirements.txt
└── spample.txt           # Example profile
```
