from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'MyDonutsApp'

    def __str__(self):
        return self.title


class MydonutsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MyDonutsApp'

