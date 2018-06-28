import dj_database_url
from scravie.settings.base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config()
}
