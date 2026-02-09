import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file FIRST, before any other imports
from dotenv import load_dotenv

env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
)
load_dotenv(env_path, override=True)

# NOW import Flask and other modules
from flask import Flask, render_template, request, jsonify
from roaster.parser import extract_text
from roaster.analyzer import analyze_profile
from roaster.roast_engine import roast_profile
from roaster.suggestions import generate_suggestions
from roaster.ai_roaster import generate_ai_roasts, generate_ai_suggestions
import tempfile

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Load configuration
try:
    from config import get_config

    app.config.from_object(get_config())
except ImportError:
    # Fallback if config.py not available
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# Log initialization (only in development)
if app.debug:
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"[Flask] Initializing in DEBUG mode... API Key present: {bool(api_key)}")
    if api_key:
        print(f"[Flask] API Key starts with: {api_key[:10]}...")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    text = ""

    # file upload takes precedence
    uploaded = request.files.get("file")
    if uploaded and uploaded.filename:
        suffix = os.path.splitext(uploaded.filename)[1] or ".txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            uploaded.save(tmp.name)
            text = extract_text(tmp.name)
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
    else:
        text = request.form.get("text", "")

    analysis = analyze_profile(text)

    # Try AI-powered roasts/suggestions, but fall back to local generators
    roasts = []
    roast_source = "ai"
    try:
        roasts = generate_ai_roasts(text, num_roasts=3)
    except Exception:
        roasts = []

    if not roasts:
        # Fallback to local deterministic roasts
        roasts = roast_profile(analysis)
        roast_source = "fallback"

    tips = []
    tips_source = "ai"
    try:
        tips = generate_ai_suggestions(text)
    except Exception:
        tips = []

    if not tips:
        tips = generate_suggestions(analysis)
        tips_source = "fallback"

    if request.headers.get("Accept") == "application/json" or request.args.get("json"):
        return jsonify(
            {
                "roasts": roasts,
                "tips": tips,
                "analysis": analysis,
                "roast_source": roast_source,
                "tips_source": tips_source,
            }
        )

    return render_template(
        "index.html",
        text=text,
        roasts=roasts,
        tips=tips,
        analysis=analysis,
        roast_source=roast_source,
        tips_source=tips_source,
    )


@app.route("/admin/set_key", methods=["POST"])
def admin_set_key():
    """Temporarily set API keys at runtime for testing.

    Security: requires header `X-ADMIN-TOKEN` equal to `SECRET_KEY`.
    Use only for local testing; do NOT expose this in production.
    """
    # If SECRET_KEY is set to a production value, require it in header.
    secret = app.config.get("SECRET_KEY")
    if secret and secret != "dev-key":
        token = request.headers.get("X-ADMIN-TOKEN")
        if not token or token != secret:
            return ("Forbidden", 403)

    openai_key = request.form.get("openai_key")
    groq_key = request.form.get("groq_key")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    return jsonify(
        {
            "status": "ok",
            "OPENAI_API_KEY_set": bool(openai_key),
            "GROQ_API_KEY_set": bool(groq_key),
        }
    )


if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=app.config.get("PORT", 8500),
        debug=app.debug,
    )


def configure_for_production():
    """Configure app for production deployment."""
    app.config["DEBUG"] = False
    app.config["TESTING"] = False
    return app
