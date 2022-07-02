from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "PUCadmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "PUCadmin.sp_app_config.CustomSPAppConfig",
    "autocompletefilter",
    "import_export",
    "organisations",
    "schools",
    "competitions",
    "taggit",
    "taggit_selectize",
    "questions",
    "django_bootstrap5",
    "frontoffice",
    "secondments",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "sp.backends.SAMLAuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "PUCadmin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "PUCadmin.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


AUTH_USER_MODEL = "organisations.User"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGES = [
    ("nl", _("Dutch")),
    ("en", _("English")),
]
LOCALE_PATHS = [
    "locale",
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SAML SP SETTINGS
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
SP_UNIQUE_USERNAMES = False
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

PRIVACY_STATEMENT_URL = (
    "https://www.ru.nl/vaste-onderdelen/privacyverklaring-radboud-universiteit/"
)

TAGGIT_TAGS_FROM_STRING = "taggit_selectize.utils.parse_tags"
TAGGIT_STRING_FROM_TAGS = "taggit_selectize.utils.join_tags"

SERVICE_REGION_ZIPS = [
    "51",
    "50",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "80",
    "81",
    "74",
    "75",
    "76",
    "38",
    "37",
    "39",
    "40",
    "41",
    "66",
    "65",
    "67",
    "68",
    "69",
    "70",
    "73",
    "72",
    "71",
]
