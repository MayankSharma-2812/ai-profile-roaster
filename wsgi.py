"""Production WSGI entry point for gunicorn."""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment
os.environ.setdefault("FLASK_ENV", "production")

# Import and configure app
from web.app import app, configure_for_production

# Apply production configuration
configure_for_production()

if __name__ == "__main__":
    app.run()
