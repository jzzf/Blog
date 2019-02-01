from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('username or password is wrong')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=20,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(
        label='email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(
        label='Verify',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'click to send verification code'}))
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(
        label='再输入一次密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('Verification Code is wrong')
        return self.cleaned_data

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

    def clear_verification_code(self):
        verificatin_code = self.cleaned_data.get('verification_code', '')
        if verificatin_code == '':
            raise forms.ValidationError('Verification Code can not be blank')
        return verificatin_code


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='new nickname',
                                   max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Input new nickname'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('User not login')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('New nickname can not be blank')


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input email'}))
    verification_code = forms.CharField(label='Verification code',
                                        required=False,
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'click to send verification code'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('User not login')

        if self.request.user.email == '':
            raise forms.ValidationError('This email has been bound')

        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('Verification Code is wrong')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email has been bound')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('Verification Code can not be blank')
        return verification_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='old password',
                                   max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Input old password'}))
    new_password = forms.CharField(label='new password',
                                   max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Input new password'}))
    new_password_again = forms.CharField(
        label='new password',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input new password'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('passwords are different')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Old password is wrong')
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input email'}))

    verification_code = forms.CharField(label='Verification code',
                                        required=False,
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'click to send verification code'}))

    new_password = forms.CharField(label='new password',
                                   max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Input new password'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('email does not exist')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('Verification Code can not be blank')

        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('forgot_password_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('Verification Code is wrong')

        return verification_code
