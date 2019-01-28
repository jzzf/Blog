from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data
from blog.models import Blog



def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    return render(request, 'home.html', context)

