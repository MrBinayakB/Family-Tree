from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fzy)x%dcm!%s!op0di^)!+&-1-5r-^umdy#bc48l2-9y(cf=z2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'apps.people',
    'apps.relationship',
    'apps.trees',
    'apps.users',
    #'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # ---------- FORMATTERS ----------
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} | {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },

    # ---------- HANDLERS ----------
    "handlers": {
        # Console (dev)
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },

        # Main app log
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/app.log",
            "formatter": "verbose",
        },

        # Errors only
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/errors.log",
            "formatter": "verbose",
        },

        # Per-app logs
        "people_file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/people.log",
            "formatter": "verbose",
        },
        "relationship_file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/relationship.log",
            "formatter": "verbose",
        },
        "trees_file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/trees.log",
            "formatter": "verbose",
        },
        "users_file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/users.log",
            "formatter": "verbose",
        },
    },

    # ---------- LOGGERS ----------
    "loggers": {
        # Default Django logger
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },

        # App-specific loggers
        "apps.people": {
            "handlers": ["console", "people_file"],
            "level": "INFO",
            "propagate": False,
        },
        "apps.relationship": {
            "handlers": ["console", "relationship_file"],
            "level": "INFO",
            "propagate": False,
        },
        "apps.trees": {
            "handlers": ["console", "trees_file"],
            "level": "INFO",
            "propagate": False,
        },
        "apps.users": {
            "handlers": ["console", "users_file"],
            "level": "INFO",
            "propagate": False,
        },
    },

    # ---------- ROOT ----------
    "root": {
        "handlers": ["console", "file", "error_file"],
        "level": "INFO",
    },
}
