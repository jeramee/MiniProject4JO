# DjangoTest3/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from ..blog.views import (base_view, index_view, page1, page2, page3, page4, page5, register_view, login_view)
# from ..blog.views import create_view  # Corrected import statement
from blog.views import (base_view, index_view, page1, page2, page3, page4, page5, register_view, login_view)
from blog.views import create_view  # Corrected import statement
# from blog import urls as blog_urls
from blog.url import urlpatterns


urlpatterns = [
    path('base/', base_view, name='base'),
    path('', index_view, name='index'),
    path('page1/', page1, name='page1'),
    path('page2/', page2, name='page2'),
    path('page3/', page3, name='page3'),
    path('page4/', page4, name='page4'),
    path('page5/', page5, name='page5'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.url')),  # Include the blog app URLs here
    path('create/', create_view, name='create'),  # Add this line for create_view
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
