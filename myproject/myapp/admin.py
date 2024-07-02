from django.contrib import admin
from .models import Author, Category, Article, Comment, Like, Contact, Visitor
from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from django.urls import path
from django.contrib import admin
from django.db.models import Count


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'author', 'category', 'published_date', 'views', 'likes')
    list_filter = ('category', 'author', 'published_date')
    search_fields = ('title', 'content')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'created_on')
    list_filter = ('article', 'created_on')
    search_fields = ('name', 'body')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'ip_address', 'created_at')
    list_filter = ('article', 'created_at')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_on')
    search_fields = ('name', 'email', 'subject')

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp')  # Adjust 'timestamp' to a valid field in Visitor model

admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Visitor , VisitorAdmin)
