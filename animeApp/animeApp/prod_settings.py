import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


SECRET_KEY = 'djang-xzjfdasfs21342354sdf$VG@WS4234@$@_f(=kws+5ab-7)g2a+3-fz*f'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static') #STATIC_ROOT будет собирать статику только тогда когда DEBUG = False