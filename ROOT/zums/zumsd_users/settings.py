DEBUG = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/zumsd_users.db'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',

    'zums.zumsd_users',
]

ROOT_URLCONF = 'zums.zumsd_users.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SESSION_ENGINE = "zums.django_backends.session"
AUTHENTICATION_BACKENDS = ["zums.django_backends.auth.ZUMSBackend"]

SECRET_KEY = 'gw2)POSOBX1Z1N4NQ-oh3kv%atu+awg@=@r!jklo@i_v&#o'

