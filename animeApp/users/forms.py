from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

if not User:
    raise ValueError('Not Found User!')


class CustomBaseForm(forms.ModelForm):
    
    def add_common_widgets(self, fields):
        for field_name in fields:
            field = self.fields[field_name]
            field.widget.attrs.update({
                "class": f"{field_name}-fields-anime",
                "placeholder": field.label
            })

class UserLoginForm(AuthenticationForm, CustomBaseForm):
    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": 'email-fields-anime',
                'placeholder': 'Email address'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": 'password-fields-anime',
                'placeholder': 'Password'
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('username', 'password')
    
        
        
class RegisterLoginForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": 'email-fields-anime',
                'placeholder': 'Username'
            }
        ),
        label="profile"
    )
    email = forms.CharField(
        widget=forms.EmailInput(
        attrs={
            "class": 'email-fields-anime',
            'placeholder': 'Email address'
            }
        ),
        label="mail"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "class": 'password-fields-anime',
            'placeholder': 'Password'
            }
        ),
        label='lock'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "class": 'password-fields-anime',
            'placeholder': 'Password Again'
            }
        ),
        label='lock'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')
        
        return email