"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from stdlib import read_file
Version='0.0.1'
if sys.platform.startswith('linux'):
    WORK_PATH='/var/www/mysite'
    CONFIG_PATH='/etc/mysite'
else:
    WORK_PATH='c:/mysite'
    CONFIG_PATH='c:/mysite'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-57v#d0i4a8box--1-jabm_o1yh!y9=1v=4r@#cee#@+%vbxv-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 添加已安装的应用
lines=read_file(os.path.join(CONFIG_PATH,'installed_apps'))
for line in lines:
    line=line[:line.find('#')].strip()
    if line:
        INSTALLED_APPS.append(line)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sitemgr.urls'

WSGI_APPLICATION = 'sitemgr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'mysite',
        'USER': 'hunter',
        'PASSWORD': '123456',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(WORK_PATH,'media')
STATIC_ROOT=os.path.join(WORK_PATH,'static')
