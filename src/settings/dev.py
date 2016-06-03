"""Development settings and globals."""

from os.path import join, normpath

from .common import *

# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION

########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
########## END TEMPLATE CONFIGURATION

########## AUTH CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"1p)g!_znl4-_8gj%)1yfm7_##%3sj87y1u6b(zcr^fa11o5h2w"
########## END AUTH CONFIGURATION

########## CELERY CONFIGURATION
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_URL = 'django://'

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERYD_CONCURRENCY = 1
########## END CELERY CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
  }
}

GRAPH_DB_URL = 'http://localhost:7474/db/data/'
GRAPH_DB_USERNAME = None
GRAPH_DB_PASSWORD = None
########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches

########## END CACHE CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging

LOGGING['handlers']['console_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.StreamHandler',
  'formatter': 'local_standard'
}

LOGGING['handlers']['file_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/app.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'formatter': 'local_standard',
  'encoding': 'UTF-8',
}

LOGGING['handlers']['request_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/django_request.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'formatter': 'local_standard',
  'encoding': 'UTF-8',
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/error.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 5,
  'formatter': 'local_standard',
  'encoding': 'UTF-8',
}

app_logger = {
  'handlers': ['console_handler', 'file_handler', 'exception_handler'],
  'level': 'DEBUG',
  'propagate': False
}

LOGGING['loggers'] = {
  '': {
    'handlers': ['console_handler', 'file_handler', 'exception_handler'],
    'level': 'DEBUG',
    'propagate': True
  },
  'django.request': {
    'handlers': ['request_handler', 'exception_handler', 'console_handler'],
    'level': 'DEBUG',
    'propagate': False
  },
  'celery': {
    'level': 'INFO',
  },
  'django.db.backends': {
    'level': 'INFO',
  },
  'src.aggregates': app_logger,
  'src.apps': app_logger,
  'src.libs': app_logger,
}
########## END LOGGING CONFIGURATION

########### SOCIAL PROVIDER CONFIGURATION
TWITTER_APP_KEY = 'Twitter app key'
TWITTER_APP_SECRET = 'Twitter app secret'

LINKEDIN_API_KEY = 'LinkedIn api key'
LINKEDIN_API_SECRET = 'LinkedIn api secret'
LINKEDIN_USER_TOKEN = 'LinkedIn user token'
LINKEDIN_USER_SECRET = 'LinkedIn user secret'
LINKEDIN_REDIRECT_URI = 'http://localhost:8000/'

FULLCONTACT_API_KEY = 'FullContact api key'

REDDIT_SUBREDDIT_QUERY_LIMIT = 2
########## END SOCIAL PROVIDER CONFIGURATION

########### NLP CONFIGURATION
ALCHEMY_API_KEY = 'Alchemy Key'
########## END NLP CONFIGURATION

########### DRIVE CONFIGURATION
DRIVE_USERNAME = 'Drive user'
DRIVE_PASSWORD = 'Drive password'
DRIVE_ASSIGNMENT_SPREADSHEET_KEY = 'Drive Spreadsheet'
########## END DRIVE CONFIGURATION

########### EMAIL CONFIGURATION
SENDGRID_USERNAME = "Test_User"
SENDGRID_PASSWORD = "Password"
########## END EMAIL CONFIGURATION

########### EXTERNAL API CONFIGURATION
MASHAPE_API_KEY = "Mashape Api Key"
########## END EXTERNAL API CONFIGURATION

# Get a developer's local overrides (if they exist)
try:
  from .dev_override import *
except:
  pass
