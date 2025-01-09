import os

from datetime import timedelta


import environ
env = environ.Env()
environ.Env.read_env()


import mimetypes
mimetypes.add_type('text/css', '.css', True)


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


if env('PROD') == 'True':

    DEBUG = False
    
    SECURE_SSL_REDIRECT = True

    STATIC_ROOT = BASE_DIR / 'static'
    
else:

    DEBUG = True
    
    SECURE_SSL_REDIRECT = False

    STATIC_ROOT = BASE_DIR / 'staticfiles'

    STATICFILES_DIRS = [ BASE_DIR / 'static' ]

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [ 'localhost', '127.0.0.1', 'ngexile.freddecgames.com' ]

CORS_ALLOWED_ORIGINS = [
    'https://fgexile.freddecgames.com',
    'http://localhost:3000',
]

INTERNAL_IPS = [ '127.0.0.1' ]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

ADMINS = [('Freddec', 'freddec.games@gmail.com')]
MANAGERS = [('Freddec', 'freddec.games@gmail.com')]

AUTH_USER_MODEL = 'accounts.User'

ACCOUNT_ACTIVATION_DAYS = 7

REGISTRATION_OPEN = True

LOGIN_REDIRECT_URL = '/lobby'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    'precise_bbcode',
    'impersonate',
    
    'corsheaders',
    
    'rest_framework',
    'rest_framework.authtoken',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    
    'myapps.accounts',
    'myapps.lobby',
    'myapps.s03',
    'myapps.s04',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]


DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'OPTIONS': {
            'options': '-c search_path=s03,s04,public'
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'CET'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [ BASE_DIR / 'locale' ]


STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_FROM_EMAIL = 'no-reply@freddecgames.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_SSL = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'myapps.api.serializers.UserRegisterSerializer',
}
