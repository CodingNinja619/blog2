# Replaced it with lambda
# But this app might come in handy in the future when I create shop part

from django.urls import path
from .import views

app_name = 'redirects'

urlpatterns = [
    path('', views.blog_redirect, name='blog_redirect'),
]