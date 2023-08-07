from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = [
    ('Mahmoud', 'occzz123@gmail.com'),
]

ALLOWED_HOSTS = ['*']


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db", # set in docker-compose.yml
        "PORT": 5432, # default postgres port
    }
}

# Security config
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True