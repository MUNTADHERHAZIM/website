from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),  # Correct slug pattern
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('search/', views.article_search, name='article_search'),
    path('like/<slug:slug>/', views.like_article, name='like_article'),
    path('comment/<slug:slug>/', views.add_comment, name='add_comment'),
    path('thanks/', views.thanks, name='thanks'),
]
