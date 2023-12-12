# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import BlogPost
import os

def blog_index_view(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

@login_required
def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # Ensure the user is logged in
            if request.user.is_authenticated:
                author = request.user
            else:
                # Handle the case where the user is not authenticated (you can redirect to login or handle it differently)
                messages.error(request, 'You need to be logged in to create a blog post.')
                return redirect('login')

            # Save blog post to the database
            BlogPost.objects.create(title=title, content=content, author=author)

            # Create the directory if it doesn't exist
            posts_directory = "templates/blog/posts/"
            os.makedirs(posts_directory, exist_ok=True)

            # Create a new HTML file
            file_path = os.path.join(posts_directory, f"{title}.html")
            with open(file_path, 'w') as file:
                file.write(f"<html><head><title>{title}</title></head><body>{content}</body></html>")

            return redirect('blog_index')
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def detail_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})


def base_view(request):
    return render(request, 'base.html')


def index_view(request):
    return render(request, 'index.html')


# Other views remain the same...


def page1(request):
    return render(request, 'page1.html', {'response': None})


def page2(request):
    return render(request, 'page2.html', {'response': None})


def page3(request):
    return render(request, 'page3.html', {'response': None})


def page4(request):
    return render(request, 'page4.html', {'response': None})


def page5(request):
    return render(request, 'page5.html', {'response': None})


def register_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == "POST":
        if not username:
            messages.error(request, 'Username is required.')
        elif not password:
            messages.error(request, 'Password is required.')
        else:
            try:
                new_user = User.objects.create_user(username=username)
                new_user.set_password(password)
                new_user.save()
            except IntegrityError:
                messages.error(request, f'User {username} is already registered.')
            else:
                return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == "POST":
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the index page or any other page after logout

