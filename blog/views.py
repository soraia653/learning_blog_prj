from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Post, User
from .forms import PostForm

# Create your views here.
def index(request):
    all_posts = Post.objects.all()

    context_dict = {
        "posts": all_posts,
    }

    return render(request, "blog/all_posts.html", context_dict)

def read_post(request, post_id):
    select_post = Post.objects.get(id=post_id)

    context_dict = {
        "post": select_post
    }

    return render(request, "blog/read_post.html", context_dict)

def new_post(request):
        
        if request.method == "POST":
            form = PostForm(request.POST)

            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = User.objects.get(username=request.user)
                new_post.save()
                return redirect("main_page")
        else:
            form = PostForm()

        context_dict = {
            "form": form,
        }

        return render(request, "blog/new_post.html", context_dict)

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirect("main_page")
        else:
            error_dict = {
                "message": "Invalid username and/or password."
            }

            return render(request, "blog/all_posts.html", error_dict)
    
    return redirect("main_page")

def logout_view(request):
    logout(request)
    return redirect("main_page")

def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")

        # make sure email is a valid email
        email = request.POST.get("email")

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e)
            return render(request, "blog/registration.html")

        # ensure password and confirmation match
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            messages.error(request, "Passwords do not match.")
            return render(request, "blog/registration.html")
        
        # create new user
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            login(request, new_user)
            return redirect("main_page")
        except IntegrityError as e:
            messages.error(request, f"Something went wrong: {e}")
            return render(request, "blog/registration.html")
    
    return render(request, "blog/registration.html")