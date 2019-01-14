from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://localhost:8000/blog/pk
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),

]