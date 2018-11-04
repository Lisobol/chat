from django import forms
from core.models import *
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm, UserChangeForm


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин')
    password = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Повторите ввод')
    email = forms.EmailField(label='Email')
    # avatar = forms.ImageField(label='avatar',required=False)



class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=50, widget=forms.TextInput(attrs={'autofocus': True,'class': 'form-control'}))
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        message = super().save(commit=False)
        message.author = self.user
        if commit:
            message.save()
        return message


class UploadFileForm(forms.Form):
    avatar = forms.ImageField()

