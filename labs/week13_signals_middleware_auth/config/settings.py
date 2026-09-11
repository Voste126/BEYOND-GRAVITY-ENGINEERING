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
    # Trace context correlation (must run first to capture all downstream logs)
    "accounts.logging.TraceContextMiddleware",
    # Django built-ins
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    # --- Custom middleware ---
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "accounts.logging.StructuredJSONFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "accounts": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "events": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
