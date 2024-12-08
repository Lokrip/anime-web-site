from uuid import uuid4

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.http import HttpRequest
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db import IntegrityError #Когда вы пытаетесь создать запись с дублирующимся значением в поле, которое должно быть уникальным будет ошибка
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .service import send

from .forms import UserLoginForm, RegisterLoginForm
from main.models import ActivateEmailModels

from .tasks import send_spam_email

User = get_user_model()

if not User:
    raise ValueError('Not Found USER!')

class LoginView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect('anime-home:home')
        context = {
            'title': 'Авторизация',
            'form': UserLoginForm()
        }
        return render(request, 'users/login.html', context)
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect('anime-home:home')
        
        form = UserLoginForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('anime-home:home')
            else:
                messages.error(request, f'Пользователя с такой почтой {username} существует')
        else:
            messages.error(request, 'Что-то пошло не так')
            
        context = {
            'title': 'Произошла Ошибка!',
            'form': form
        }
        
        return render(request, 'users/login.html', context)

class RegisterView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect('anime-home:home')
        
        
        context = {
            'title': 'Регистрация',
            'form': RegisterLoginForm()
        }
        return render(request, 'users/register.html', context)
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect('anime-home:home')
        
        form = RegisterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            
            
            if not all([username, email, password1, password2]):
                raise ValueError("All fields are required")
            
            if password1 != password2:
                form.add_error('password2', 'Passwords do not match')
                return render(request, 'users/register.html', {'form': form, "title": 'Errors Form!'})
            
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.is_active = False
            user.set_password(password1)
            user.save()
            
            confirmation_code = get_random_string(64)
            # slug = f"{username}-code-{uuid4().hex[:8]}"
            activate_models = ActivateEmailModels.objects.create(
                confirmation_code=confirmation_code,
                status=True,
                user=user
            )
            activate_models.save()
            
            activation_link = request.build_absolute_uri(f'/account/activate/{confirmation_code}/')
            
            # delay делает так он не будет ждать ответа от форму а просто отправит ее в 
            # брокер и у нас доступ к сайту будет, и мы не будем ждать ответа 
            # тоесть просто все проходит в фоне 
            send_spam_email.delay(
                user.email,
                activation_link
            )
            
            return render(request, 'users/register.html', {'form': form, "title": 'Send mail!'})

        form.add_error('username', 'A user with that username or email already exists')
        return render(request, 'users/register.html', {'form': form, "title": 'Errors Form!'})
            
            
class ActivateAccountView(View):
    def get(self, request, confirmation_code):
        try:
            activate_models = ActivateEmailModels.objects.get(confirmation_code=confirmation_code)
            activate_models.user.is_active = True
            activate_models.user.save()

            login(request, activate_models.user)
            return redirect('anime-home:home')
        except ActivateEmailModels.DoesNotExist:
            messages.error(request, 'Invalid activation code.')
            return redirect('users:register')