from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import BlogPost
from .forms import BlogForm

def index(request):
    """The home page for the blog"""
    return render(request, 'blogs/index.html')

def posts(request):
    """Show all blogposts, abreviated"""
    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

def post(request, post_id):
    """Show single post"""
    post = BlogPost.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    """Add a new post"""
    if request.method != 'POST':
        #No data submitted; create a blank form
        form = BlogForm()
    else:
        #POST data submitted; process data
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:posts')
    
    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing post"""
    post = BlogPost.objects.get(id=post_id)
    check_topic_owner(post, request)
    
    if request.method != 'POST':
        #Initial request; pre-fill form with the current post
        form = BlogForm(instance=post)
    else:
        #POST data submitted, process data
        form = BlogForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)
    
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def check_topic_owner(post, request):
    if post.owner != request.user:
        raise Http404