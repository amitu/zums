DEBUG = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/zums_jd_test_project.db'
INSTALLED_APPS = ['zums_jd_test_project']
ROOT_URLCONF = 'zums_jd_test_project.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)
SESSION_ENGINE = "zums.django_backends.session"
SECRET_KEY = 'gw2)POSOBX1Z1N4NQ-oh3kv%atu+awg@=@r!jklo@i_v&#o'

