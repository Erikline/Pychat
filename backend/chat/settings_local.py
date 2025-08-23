import logging.config
import os

from chat.settings_base import *

DEBUG = True
TEMPLATE_DEBUG = True
SECRET_KEY = '8ou!cqb1yd)6c4h0i-cxjo&@@+04%4np6od8qn+z@5b=6)!v(o'
class InvalidString(str):
	def __mod__(self, other):
		from django.template.base import TemplateSyntaxError
		raise TemplateSyntaxError(
			"Undefined variable or unknown value for: %s" % other)

TEMPLATE_STRING_IF_INVALID = InvalidString("%s")
TEMPLATES[0]['OPTIONS']['loaders'] = [
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
]

CRT_PATH = os.sep.join((PROJECT_DIR, os.pardir, "..", "frontend", "build", "certs", "server.crt.pem"))
KEY_PATH = os.sep.join((PROJECT_DIR, os.pardir, "..", "frontend", "build", "certs", "private.key.pem"))
TORNADO_SSL_OPTIONS = {
	"certfile": CRT_PATH,
	"keyfile": KEY_PATH
}

# Prevent host header attacks in emails
SERVER_ADDRESS = 'http://localhost:8080' 
SHOW_COUNTRY_CODE = True

LOGGING['handlers'] = {
	'default': {
		'level': 'DEBUG',
		'class': 'logging.StreamHandler',
		'filters': ['id', ],
		'formatter': 'django',
	},
}

LOGGING['loggers'] = {
	'': {
		'handlers': ['default', ],
		'level': 'DEBUG',
		'propagate': False,
	},
}

# Don't close socket if we're in debug
PING_CLOSE_JS_DELAY = 100000

# 开发环境使用SQLite数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# CORS配置 - 允许前端开发服务器访问
INSTALLED_APPS = list(INSTALLED_APPS) + ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://localhost:8080",
    "https://127.0.0.1:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

logging.config.dictConfig(LOGGING)
