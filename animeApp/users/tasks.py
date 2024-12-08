from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from animeApp.celery import app
from animeApp.settings import EMAIL_HOST_USER

from celery import shared_task

from .service import send


User = get_user_model()

@app.task #Этот декоратор будет говорить Celery что это таска, ее надо отслеживать и потом её нужно запустить
def send_spam_email(user_email, activation_link): #если мы передаем что то в задачу на нельзя передовать обекты форм модели обекта и тд передовать надо определенные поля модели форму или же просто строки
    send(user_email, activation_link)
    
    
@app.task
def send_beat_email():
    for user in User.objects.all():
        send_mail(
            "Вы подписались на рассылку",
            'Какойта текст',
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        
        
@app.task
def my_task(a, b):
    c = a + b
    return c

@app.task
def my_task_as(d, e):
    c = d + e
    return c

# В Celery, параметр bind=True используется для привязки задачи к самому 
# объекту задачи. Когда вы добавляете bind=True в декоратор @app.task, это 
# позволяет внутри функции задачи (например, my_task_retry) 
# обращаться к экземпляру самой задачи через первый параметр — self. 

#max_retries максимальное каличество повторений
#Выполнение задачи повтороно через некоторое время обычны задчи протсо выполнились если выдеть исключенние они упадту и больше не подыматься
@app.task(bind=True, default_retry_delay=5 * 60, max_retries=3) #bind тоесть мы связываем нашу задачу, default_retry_delay тоесть этот параметер будет запускать повторно задачи по времени каторую мы туда укажем например при ошибки мы делаем так чтобы задача повторно запустилась через self.retry(exc=exc, countdown=60)
def my_task_retry(self, x, y):
    try:
        return x + y
    except Exception as exc:
        # exc=exc: Передает исключение (exc) в метод retry. 
        # Это исключение будет зарегистрировано в Celery и указано как причина 
        # повторного запуска задачи. Вы можете передать любое исключение, 
        # которое произошло в блоке try, например, сетевую ошибку или таймаут
        
        # countdown=60: Определяет задержку перед повторным запуском 
        # задачи в секундах (в данном случае, 60 секунд). 
        # Таким образом, Celery повторит задачу через 60 секунд после сбоя
        # тоесть мы можем по умолчанию укозать default_retry_delay=5 * 60
        # а через countdown поменять время повторнго выолнение задачи например теперь будет 60 секунд
        raise self.retry(exc=exc, countdown=60) #retry он делаеть повтроный вызов задачи



@shared_task() #shared_task это таже самая задача как @app.task разница в том что если мы пишем какойта скрипт или библеотка и нам не надо взоимодейстовать с приложение app и кратко пишем этот декоратор
def my_sh_task(msg):
    return msg + '!!!'