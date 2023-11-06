from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.urls import reverse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from .models import Post

def load_logged_in_user(request):
    user_id = request.session.get('user_id')

    if user_id is None:
        request.user = None
    else:
        request.user = User.objects.get(id=user_id)


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
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

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Incorrect username.')
        elif not user.check_password(password):
            messages.error(request, 'Incorrect password.')
        else:
            auth_login(request, user)
            return redirect('index')
    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

def index(request):
    posts = Post.objects.select_related('author').order_by('-created')
    return render(request, "index.html", {'posts': posts})

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

def get_post(id, request, check_author=True):
    try:
        post = Post.objects.select_related('author').get(pk=id)
        if check_author and post.author.id != request.user.id:
            raise PermissionDenied
        return post
    except Post.DoesNotExist:
        raise Http404(f"Post id {id} doesn't exist.")

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
    if not title:
        messages.error(request, "Title is required.")
    else:
        Post.objects.create(title=title, body=body, author=request.user)
        return redirect(reverse('blog:index'))

    return render(request, "create.html")

@login_required
def update(request, id):
    post = get_post(id, request)

    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
    if not title:
        messages.error(request, "Title is required.")
    else:
        post.title = title
        post.body = body
        post.save()
        return redirect(reverse('blog:index'))

    return render(request, "update.html", {'post': post})

@login_required
def delete(request, id):
    post = get_post(id, request)
    post.delete()
    return redirect(reverse('index'))