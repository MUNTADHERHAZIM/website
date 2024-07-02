from django.shortcuts import redirect, render, get_object_or_404
from .models import Article, Category, Comment, Like, Author, Contact ,Visitor
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import View
from .forms import CommentForm
from django.db.models import Q
from .models import Article, Category, Tag
def home(request):
    # Register visitor
    visitor_ip = request.META.get('REMOTE_ADDR')
    Visitor.objects.create(ip_address=visitor_ip)

    # Calculate counts
    visitor_count = Visitor.objects.count()
    author_count = Author.objects.count()
    article_count = Article.objects.count()

    context = {
        'visitor_count': visitor_count,
        'author_count': author_count,
        'article_count': article_count,
    }
    
    articles = Article.objects.order_by('-published_date')[:5]
    return render(request, 'home.html', {'articles': articles, 'context': context})


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        return HttpResponseRedirect(reverse('thanks'))
    return render(request, 'contact.html')

# def article_list(request):
#     articles = Article.objects.all()
#     return render(request, 'article_list.html', {'articles': articles})
def article_list(request):
    visitor_ip = request.META.get('REMOTE_ADDR')
    Visitor.objects.create(ip_address=visitor_ip)
    
    visitor_count = Visitor.objects.count()
    author_count = Author.objects.count()
    article_count = Article.objects.count()

    articles = Article.objects.order_by('-published_date')[:5]

    context = {
        'articles': articles,
        'visitor_count': visitor_count,
        'author_count': author_count,
        'article_count': article_count,
    }
    return render(request, 'article_list.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Article

from django.shortcuts import render, get_object_or_404
from .models import Article

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.views = F('views') + 1
    article.save()
    article.refresh_from_db()
    context = {
        'article': article,
    }
    related_articles = Article.objects.filter(tags__in=article.tags.all()).exclude(id=article.id)[:5]
    return render(request, 'article_detail.html', {'article': article, 'related_articles': related_articles})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'articles': articles})

# def author_detail(request, pk):
#     author = get_object_or_404(Author, pk=pk)
#     articles = Article.objects.filter(author=author)
#     return render(request, 'author_detail.html', {'author': author, 'articles': articles})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    articles = Article.objects.filter(author=author)
    
    total_views = sum(article.views for article in articles)
    total_comments = sum(article.comments.count() for article in articles)

    context = {
        'author': author,
        'articles': articles,
        'total_views': total_views,
        'total_comments': total_comments,
    }

    return render(request, 'author_detail.html', context)

def article_search(request):
    query = request.GET.get('q')
    category_name = request.GET.get('category')
    tag_name = request.GET.get('tag')

    articles = Article.objects.all()

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    if category_name:
        articles = articles.filter(category__name__icontains=category_name)

    if tag_name:
        articles = articles.filter(tags__name__icontains=tag_name)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'query': query
    }
    return render(request, 'article_search.html', context)

# def article_search(request):
#     query = request.GET.get('q')
#     category = request.GET.get('category')
#     tag = request.GET.get('tag')
#     articles = Article.objects.all()
#     if query:
#         articles = articles.filter(title__icontains=query)
#     if category:
#         articles = articles.filter(category__name__icontains=category)
#     if tag:
#         articles = articles.filter(tags__name__icontains=tag)
#     if query:
        
#         articles = Article.objects.filter(
#             Q(title__icontains=query) |  # بحث في العنوان
#             Q(summary__icontains=query) |  # بحث في الملخص
#             Q(content__icontains=query)  # بحث في المحتوى
#         ).distinct()  # التأكد من عدم عرض نتائج مكررة

#         context = {
#             'articles': articles,
#             'query': query
#         }
#         return render(request, 'article_search.html', context)
#     else:
#         return render(request, 'article_search.html', {'articles': [], 'query': query})
def like_article(request, slug):
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        
        # التحقق من عدم وجود إعجاب مسبق من نفس العنوان IP
        ip_address = request.META.get('REMOTE_ADDR')
        if Like.objects.filter(article=article, ip_address=ip_address).exists():
            return redirect('article_detail', slug=slug)
        
        # إنشاء مثيل جديد لـ Like
        like = Like(article=article, ip_address=ip_address)
        like.save()
        
        # زيادة عدد الإعجابات في المقال
        article.likes += 1
        article.save()
        
        # إعادة توجيه المستخدم إلى صفحة تفاصيل المقال
        return redirect('article_detail', slug=slug)
    
    # إذا لم يكن الطلب POST، يمكنك تنفيذ ما تراه مناسبًا هنا، مثلاً ربما رسالة خطأ أو توجيه إلى صفحة أخرى.
    return redirect('article_detail', slug=slug)  # مثال بسيط للتوضيح

def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
        Comment.objects.create(article=article, name=name, body=body, parent=parent_comment)
    return HttpResponseRedirect(reverse('article_detail', args=[slug]))

def thanks(request):
    return render(request, 'thanks.html')


class AddCommentView(View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.ip_address = request.META.get('REMOTE_ADDR')
            comment.save()
        return redirect('article_detail', slug=slug)