
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('blog:post_list'), name='blog_redirect'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace='account')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
