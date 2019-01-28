from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('username or password is wrong')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=20,
                               min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='email',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(label='再输入一次密码',
                                     widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username has been used')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email has been used')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('password does not match')
        return password_again
