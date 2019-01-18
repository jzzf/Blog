from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data
from blog.models import Blog
from .forms import LoginForm


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
                user = login_form.cleaned_data['user']
                auth.login(request, user)
                return redirect(request.GET.get('from'), reverse('home'))
    else:

        login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)
