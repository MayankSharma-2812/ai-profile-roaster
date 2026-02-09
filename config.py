"""Production-ready configuration for AI Profile Roaster."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8500))

    # File Upload
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))  # 10MB
    UPLOAD_FOLDER = "/tmp"

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Security
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False
    # Do not assert for API keys at import time; runtime checks should
    # validate keys where the services are called. This avoids import
    # failures in environments where keys are injected later.


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    OPENAI_API_KEY = "test-key"
    GROQ_API_KEY = "test-key"


# Select configuration based on environment
def get_config():
    """Return appropriate config based on FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "production").lower()

    if env == "development":
        return DevelopmentConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return ProductionConfig()
