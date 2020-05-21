from django.shortcuts import render

from .models import BlogPost

def index(request):
    """The home page for the blog"""
    return render(request, 'blogs/index.html')

def posts(request):
    """Show all blogposts, abreviated"""
    posts = BlogPost.objects.order_by('date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

def post(request, post_id):
    """Show single post"""
    post = BlogPost.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'blogs/post.html', context)