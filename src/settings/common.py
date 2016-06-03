"""Common settings and globals."""
"""Common settings and globals."""
from celery.app.log import TaskFormatter

from datetime import timedelta
from os import environ
from os.path import abspath, basename, dirname, join, normpath
from sys import path
from kombu.serialization import register
from src.libs.django_utils.serialization.json_serializer_registration import json_flex_dumps, json_flex_loads
from src.settings import constants
from os.path import abspath, dirname, basename
# from src.libs.python_utils.logging.rq_formatter import RqFormatter

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name:
SITE_NAME = basename(DJANGO_ROOT)
########## END PATH CONFIGURATION

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

CONSTANTS = constants
########## END GENERAL CONFIGURATION

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
  'django.middleware.gzip.GZipMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
)
########## END MIDDLEWARE CONFIGURATION

########## TEMPLATE CONFIGURATION
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
########## END TEMPLATE CONFIGURATION

########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url

STATIC_URL = '/static/'
########## END STATIC FILE CONFIGURATION

########## APP CONFIGURATION
DJANGO_APPS = (
  # Default Django apps:
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
  # Static file management:

  # Asynchronous task queue:
  'djcelery',
  'kombu.transport.django',

  # Database

  # Analytics

  # Rest API

  # Headers
)

LOCAL_APPS = (
  # AGGREGATES
  'src.domain.client',
  'src.domain.engagement_assignment',
  'src.domain.engagement_opportunity',
  'src.domain.profile',
  'src.domain.prospect',
  'src.domain.topic',

  # APPS
  'src.apps.assignment_delivery',
  'src.apps.domain',
  'src.apps.engagement_discovery',
  'src.apps.graph',

  # LIBS
  'src.libs.common_domain',
  'src.libs.django_utils',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# celery hijacks its logging to prevent other libs from screwing it up. In dev only, it'd be nice to write to a log
# file.
# http://docs.celeryproject.org/en/latest/configuration.html#logging
# why: http://stackoverflow.com/a/6942030/173957
# code: /celery/app/log.py
# if self.app.conf.CELERYD_HIJACK_ROOT_LOGGER:
#  root.handlers = []

# celery controls the root logging behavior with --loglevel=LEVEL
# we've set it to DEBUG so that our app controls the levels.

CELERYD_HIJACK_ROOT_LOGGER = False
# why celery logs all as warning: http://stackoverflow.com/questions/12664250/celery-marks-all-output-as-warning
CELERY_REDIRECT_STDOUTS = False

# todo - only use taskformatter class when celery is running - consider doing this in celery_app.py
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'standard': {
      '()': TaskFormatter,
      'fmt': '[%(levelname)s/%(processName)s/%(process)s] [%(task_name)s(%(task_id)s)] %(name)s: %(message)s'
    },
    'local_standard': {
      '()': TaskFormatter,
      'fmt': '[%(asctime)s: %(levelname)s/%(processName)s/%(process)s] [%(task_name)s(%(task_id)s)] %(name)s: %(message)s'
    },
  },
  'handlers': {}
}
########## END LOGGING CONFIGURATION


########## CELERY CONFIGURATION
CELERY_LONGEST_RUNNING_TASK_SECONDS = 60 * 60 * 48  # seconds * minutes * hours = 2 days
# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(seconds=CELERY_LONGEST_RUNNING_TASK_SECONDS)

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYD_TASK_TIME_LIMIT = 60 * 20  # seconds * minutes = 20 min
# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-accept-content
# 3.2 is going to remove pickle http://docs.celeryproject.org/en/latest/whatsnew-3.1.html#last-version-to-enable
# -pickle-by-default

register('json', json_flex_dumps, json_flex_loads,
         content_type='application/json',
         content_encoding='utf-8')

CELERY_TASK_SERIALIZER = 'json'

CELERY_IMPORTS = (
  'src.apps.engagement_discovery.services.engagement_discovery_tasks',
  'src.apps.assignment_delivery.services.assignment_delivery_tasks',
  'src.apps.domain.engagement_assignment.services.assigned_prospect_tasks',
  'src.apps.maintenance.database.services.database_maintenance_tasks',
  'src.domain.client.services.client_tasks',
)

# See: http://docs.celeryproject.org/en/master/configuration.html#celery-acks-late
CELERY_ACKS_LATE = True
########## END CELERY CONFIGURATION

########### SOCIAL PROVIDER CONFIGURATION
REDDIT_USER_AGENT = 'WiFL v0.1 https://github.com/WiFL-co'
REDDIT_SUBREDDIT_QUERY_LIMIT = 10
########## END SOCIAL PROVIDER CONFIGURATION

########### EXTERNAL API CONFIGURATION
HTTP_TIMEOUT = 10  # seconds
########## END EXTERNAL API CONFIGURATION

########### REDIS QUEUE CONFIGURATION
# The actual config of the redis cache location is env-specific. However, the queues themselves are app specific.
# Within our app, we'll decide whether to use high, default, low.
RQ_QUEUES = {
  'high': {
    'USE_REDIS_CACHE': 'default',
  },
  'default': {
    'USE_REDIS_CACHE': 'default',
  }
}
########## END REDIS QUEUE CONFIGURATION
