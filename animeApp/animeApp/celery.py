import os
from celery import Celery
from celery.schedules import crontab

# Указываем где находиться DJANGO_SETTIGNS_MODULE и настройки джанго приложение
# Устанавливаем переменную окружения для настроек Django как в manage.py

# Это нужно для того чтобы в самом файле settings.py мы могли прописовать
# Некие настройки для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animeApp.settings')

# Создаем объект celery и передаем в него некое имя
app = Celery('animeApp')

# Это нужно чтобы Celery мог работать с джанго namespace нужен чтобы при создание
# переменной она должна сначало писать CELERY и потом имя перемное тоесть
# "CELERY_ИМЯ_ПЕРЕМЕННОЙ"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Это нужно чтобы автоматический поцыплять наши таски тоесть задачи
app.autodiscover_tasks()

# Этот код настраивает планировщик задач для приложения, использующего 
# Celery (фреймворк для управления асинхронными задачами). 
# Конфигурация beat_schedule отвечает за расписание выполнения определённой задачи с 
# использованием Celery Beat, который периодически запускает задачи по расписанию
app.conf.beat_schedule = {
    'send-spam-every-10-minute': { #имя таски
        'task': 'users.tasks.send_beat_email', #наша таска каторая будет выполняться в папке users.tasks.send_beat_email вот этот файл такски send_beat_email
        'schedule': crontab(minute='*/5') #интервал выполение задачи(таска)
    }
}