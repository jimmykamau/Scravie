import dj_database_url
from scravie.settings.base import *

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'scravie-staging.herokuapp.com'
]

DATABASES = {
    'default': dj_database_url.config()
}
