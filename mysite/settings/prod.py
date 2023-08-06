from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = [
    ('Mahmoud', 'occzz123@gmail.com'),
]

ALLOWED_HOSTS = ['.vercel.app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "db", # set in docker-compose.yml
#         "PORT": 5432, # default postgres port
#     }
# }

# Security config
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True