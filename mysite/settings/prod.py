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

# AWS config
AWS_ACCESS_KEY_ID = 'AKIAZP6WZFS3VDLUZ5EL'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'invoices-management-demo'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# For static files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# For media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Security config
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True