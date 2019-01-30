import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm
from .models import Profile

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
                user = login_form.cleaned_data['user']
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
    else:

        login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()

            user = auth.authenticate(request, username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:

        reg_form = RegForm()
    context = {'reg_form': reg_form}
    return render(request, 'user/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = 'Change Nickname'
    context['form_title'] = 'Change Nickname'
    context['submit_text'] = 'Change'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = 'Bind Email'
    context['form_title'] = 'Bind Email'
    context['submit_text'] = 'Bind'
    context['form'] = form
    context['return_back_url'] = redirect_to

    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', '')
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

            send_mail(
                'Bind Email',
                'Verification Code %s' % code,
                'zhaoyli311@gmail.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)

