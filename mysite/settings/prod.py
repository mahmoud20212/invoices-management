from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = [
    ('Mahmoud', 'occzz123@gmail.com'),
]

ALLOWED_HOSTS = ['*']


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": "TxWfipBM5jLlNKjPACFN",
        "HOST": "containers-us-west-130.railway.app",
        "PORT": 5838,
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

# Rabbitmq config
# RABBITMQ = {
#     "PROTOCOL": "amqp", # in prod change with "amqps"
#     "HOST": os.getenv("RABBITMQ_HOST", "rabbitmq"),
#     "PORT": os.getenv("RABBITMQ_PORT", 5672),
#     "USER": os.getenv("RABBITMQ_USER", "guest"),
#     "PASSWORD": os.getenv("RABBITMQ_PASSWORD", "guest"),
# }

# Celery config
# CELERY_BROKER_URL = f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}/"
CELERY_BROKER_URL = "redis://default:yEMviez2LFVJsDklKOR8@containers-us-west-61.railway.app:5570"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://default:W5eHYGZAxiSfrSM5K37S@containers-us-west-61.railway.app:7595'

# django-db
# Security config
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True