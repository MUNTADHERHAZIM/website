from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='authors/', blank=True, null=True)
    social_media_links = models.JSONField(default=dict, blank=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=100, blank=True, null=True)
    facebook_handle = models.CharField(max_length=100, blank=True, null=True)
    instagram_handle = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def article_count(self):
        return self.articles.count()
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    summary = models.TextField(max_length=500)
    content = HTMLField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='images/',
                                processors=[ResizeToFill(800, 600)],
                                format='JPEG',
                                options={'quality': 90})
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)  # تغيير اسم الحقل هنا
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def article_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    @property
    def read_time_minutes(self):
        words_per_minute = 200  # assuming an average reading speed of 200 words per minute
        total_words = len(self.content.split())
        return int(total_words / words_per_minute)

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def like_count(self):
        return self.likes.count()  # تغيير هنا ليتناسب مع اسم الحقل الجديد
    
    @property
    def time_since_published(self):
        now = timezone.now()
        diff = now - self.published_date
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 0:
            return f"{days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "Just now"

        
class Comment(models.Model):
    article = models.ForeignKey('Article', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    body = models.TextField()
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # make it optional
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.name}'


class Like(models.Model):
    article = models.ForeignKey('Article', related_name='article_likes', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('article', 'ip_address')

    def __str__(self):
        return f'Like from {self.ip_address} on {self.article}'
    
    
class Like(models.Model):
    article = models.ForeignKey('Article', related_name='article_likes', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('article', 'ip_address')

    def __str__(self):
        return f'Like from {self.ip_address} on {self.article}'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Visitor from {self.ip_address} at {self.timestamp}'