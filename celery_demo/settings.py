"""
Django settings for celery_demo project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from datetime import timedelta
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '43#^z$bq$%9k8mktfm)%uu8zy-5kv)g6)e0&q0!0=#&85m)8c7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Admin.apps.AdminConfig',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'celery_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'celery_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CELERY_TIMEZONE='Asia/Shanghai'  #并没有北京时区，与下面TIME_ZONE应该一致
BROKER_URL='redis://127.0.0.1:6379/1'  #任何可用的redis都可以，不一定要在django server运行的主机上
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  ###
CELERY_BEAT_SCHEDULER = 'django-celery-beat.schedulers.DatabaseScheduler'  # 定时任务调度器
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERY_ENABLE_UTC = True # 不是用UTC
# CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TASK_RESULT_EXPIRES = 10 #任务结果的时效时间
CELERYD_MAX_TASKS_PER_CHILD = 3 #  每个worker最多执行3个任务就会被销毁，可防止内存泄露

#日志配置
# CELERYD_LOG_FILE = BASE_DIR + "/logs/celery/celery.log" # log路径
# CELERYBEAT_LOG_FILE = BASE_DIR + "/logs/celery/beat.log" # beat log路径
# CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml'] # 允许的格式


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

# 汉化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# celery beat相关
CELERY_BEAT_SCHEDULE = {
    "test1": {
        # "task": "mypro.app01.tasks.mul",  #执行的函数.这里是绝对引入的方式,在INSTALLED_APPS中注册app01时要这样注册:"mypro.app01",不过试了一下这样不行,worker启动报错.
        "task": "app01.tasks.mul",  # 执行的函数,这里要注意引入方式,要和tasks.py文件的归属app在INSTALLED_APPS中注册app的引入方式一致,这里使用的是相对引入.
        "schedule": timedelta(seconds=5),  # every minute 每分钟执行
        "args": (2, 3)  # # 任务函数参数
    },

    "test2": {

        "task": "app01.tasks.add",
        # "schedule": crontab(minute=0, hour="*/1"),   # every minute 每小时执行
        "schedule": crontab(minute="*/1"),  # every minute 每小时执行
        "args": (23, 43)
    },
}
# celery beat相关end