from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from shop.forms import RegisterForm


@login_required()
def profile_user(request):
    data = {
        "path": "Profile"
    }
    return render(request, 'shop/profile.html', context=data)

def login_user(request):
    data = {
        "path": "Login"
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'shop/login.html', context=data)

def logout_user(request):
    logout(request)
    return redirect('dashboard')

def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            reset_password = form.cleaned_data.get('reset_password')

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(reset_password)
            user.save()
            return redirect('login_user')

    data = {
        "path": "Register",
        "form": form
    }
    return render(request, 'shop/register.html', context=data)