import os

from .base import *

SECRET_KEY = "django-insecure-g&nd0j85uq*0+^wopp^&rko5tvrau#p_iwz^&5lj65xe0o!r@("

DEBUG = True

ALLOWED_HOSTS = []


# Databases
# https://docs.djangoproject.com/en/3.2/ref/databases/

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Email
# https://docs.djangoproject.com/en/3.2/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_DEFAULT_SENDER = "development@example.com"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
