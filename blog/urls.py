from django.urls import path
from .import views
from livereload import Server
from django.core.wsgi import get_wsgi_application


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('search/', views.post_search, name='post_search'),
    path('tag/<slug:tag_slug>/', views.post_list, name='posts_by_tag'),
    path('create/', views.post_create, name='create'),
    path('post/add-in-read-later/', views.add_in_read_later, name='add_in_read_later'),
    path('read-later/', views.read_later, name='read_later'),
]
