"""Minimal Django settings for the Week 13 lab."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "week13-lab-insecure-dev-key-do-not-use-in-production"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "accounts",
    "events",
]

MIDDLEWARE = [
    # Django built-ins (order matters)
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    # --- Your custom middleware (Task 2) ---
    "events.middleware.RequestTimingMiddleware",
    "events.middleware.OrganizationMiddleware",
]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Use the default User model
AUTH_USER_MODEL = "auth.User"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.OrganizationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Silence Django system-check warnings about missing templates config
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]
