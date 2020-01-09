from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Comment

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment, MarkdownxModelAdmin)
