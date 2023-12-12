# blog/urls.py
from django.urls import path
from .views import index_view, create_view, detail_view

urlpatterns = [
    path('', index_view, name='blog_index'),
    path('create/', create_view, name='blog_create'),
    path('<int:pk>/', detail_view, name='blog_detail'),
    # Add more paths for other views as needed
]
