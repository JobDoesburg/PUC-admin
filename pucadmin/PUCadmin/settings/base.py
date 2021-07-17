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
    #"django_saml2_auth",
    "autocompletefilter",
    "import_export",
    "organisations",
    "schools",
    "competitions",
    "questions",
    "django_bootstrap5",
    "frontoffice",
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
    ('nl', _('Dutch')),
    ('en', _('English')),
]
LOCALE_PATHS = [
    "locale",
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# SAML
# https://pypi.org/project/django-saml2-auth/

SAML2_AUTH = {
    # Metadata is required, choose either remote url or local file path
    "METADATA_LOCAL_FILE_PATH": "saml-metadata.xml",
    # Optional settings below
    "DEFAULT_NEXT_URL": "/",  # Custom target redirect URL after the user get logged in. Default to /admin if not set. This setting will be overwritten if you have parameter ?next= specificed in the login URL.
    "CREATE_USER": "TRUE",  # Create a new Django user when a new user logs in. Defaults to True.
    "NEW_USER_PROFILE": {
        "USER_GROUPS": [],  # The default group name when a new user logs in
        "ACTIVE_STATUS": False,  # The default active status for new users
        "STAFF_STATUS": True,  # The staff status for new users
        "SUPERUSER_STATUS": False,  # The superuser status for new users
    },
    "ATTRIBUTES_MAP": {  # Change Email/UserName/FirstName/LastName to corresponding SAML2 userprofile attributes.
        "email": "mail",
        "username": "uid",
        "first_name": "displayName",
    },
    "TRIGGER": {
        # 'CREATE_USER': 'path.to.your.new.user.hook.method',
        # 'BEFORE_LOGIN': 'path.to.your.login.hook.method',
    },
    "ASSERTION_URL": "https://puc-admin.science.ru.nl/saml2_auth/acs",  # Custom URL to validate incoming SAML requests against
    "ENTITY_ID": "puc-admin.science.ru.nl",  # Populates the Issuer element in authn request
    "NAME_ID_FORMAT": "uid",  # Sets the Format property of authn NameIDPolicy element
    "USE_JWT": False,  # Set this to True if you are running a Single Page Application (SPA) with Django Rest Framework (DRF), and are using JWT authentication to authorize client users
    "FRONTEND_URL": "puc-admin.science.ru.nl",  # Redirect URL for the client if you are using JWT auth with DRF. See explanation below
}
