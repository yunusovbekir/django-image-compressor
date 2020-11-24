import glob
import os
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'test_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

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

settings.configure(
    SECRET_KEY="test_secret_key",
    DEBUG=False,
    TEMPLATE_DEBUG=False,
    ALLOWED_HOSTS=[],
    INSTALLED_APPS=INSTALLED_APPS,
    MIDDLEWARE=MIDDLEWARE_CLASSES,
    ROOT_URLCONF='tests.urls',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    TEMPLATES=TEMPLATES,
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    STATIC_URL='/static/',
    PASSWORD_HASHERS=(
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ),
    FIXTURE_DIRS=glob.glob(BASE_DIR + '/' + '*/fixtures/')
)

django.setup()
args = [sys.argv[0], 'test']
# Current module (``tests``) and its submodules.
test_cases = '.'

# Allow accessing test options from the command line.
offset = 1
try:
    sys.argv[1]
except IndexError:
    pass
else:
    option = sys.argv[1].startswith('-')
    if not option:
        test_cases = sys.argv[1]
        offset = 2

args.append(test_cases)
# ``verbosity`` can be overwritten from command line.
args.append('--verbosity=2')
args.extend(sys.argv[offset:])

execute_from_command_line(args)
