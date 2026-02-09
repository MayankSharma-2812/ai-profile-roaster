import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file FIRST, before any other imports
from dotenv import load_dotenv

env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
)
load_dotenv(env_path, override=True)

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
print(f"[Flask] Initializing... API Key present: {bool(api_key)}")
if api_key:
    print(f"[Flask] API Key starts with: {api_key[:10]}...")

# NOW import Flask and other modules
from flask import Flask, render_template, request, jsonify
from roaster.parser import extract_text
from roaster.analyzer import analyze_profile
from roaster.roast_engine import roast_profile
from roaster.suggestions import generate_suggestions
from roaster.ai_roaster import generate_ai_roasts, generate_ai_suggestions
import tempfile

app = Flask(__name__, static_folder="static", template_folder="templates")


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

    # Generate ONLY AI roasts - no fallback
    roasts = generate_ai_roasts(text, num_roasts=3)
    if not roasts:
        roasts = ["[ERROR] AI roasts failed. Check API key or API status."]

    # Generate ONLY AI suggestions - no fallback
    tips = generate_ai_suggestions(text)
    if not tips:
        tips = ["[ERROR] AI suggestions failed. Check your OpenAI API key."]

    if request.headers.get("Accept") == "application/json" or request.args.get("json"):
        return jsonify({"roasts": roasts, "tips": tips, "analysis": analysis})

    return render_template(
        "index.html", text=text, roasts=roasts, tips=tips, analysis=analysis
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8500, debug=True)
