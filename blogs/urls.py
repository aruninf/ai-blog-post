from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blog_id>', views.blog_update, name='blog_update'),
    path('blog_delete/<int:blog_id>', views.blog_delete, name='blog_delete'),
    ]