from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


admin.site.register(BlogPost, BlogPostAdmin)

