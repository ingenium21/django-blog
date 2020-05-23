from django.shortcuts import render, redirect

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

def new_post(request):
    """Add a new post"""
    if request.method != 'POST':
        #No data submitted; create a blank form
        form = BlogForm()
    else:
        #POST data submitted; process data
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:posts')
    
    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)