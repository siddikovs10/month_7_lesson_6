from django import forms
from django.contrib.auth.models import User
import re

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form__input", "placeholder":"First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form__input", "placeholder":"Last Name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form__input", "placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form__input", "placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form__input", "placeholder":"Password"}))
    reset_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form__input", "placeholder":"Confirm Password"}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError("Username is required")
        if len(username) < 6:
            raise forms.ValidationError("Username must be at least 6 characters long")
        if ' ' in username:
            raise forms.ValidationError("Username must not contain spaces")
        if not re.match("^[A-Za-z0-9_]+$", username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError("Email is required")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Enter a valid email address")
        return email
    
    def clean_reset_password(self):
        password = self.cleaned_data.get('password')
        reset_password = self.cleaned_data.get('reset_password')
        if password is None:
            raise forms.ValidationError("Password is required")
        if reset_password is None:
            raise forms.ValidationError("Please confirm your password")
        if password == "12345678" or password == "password" or password == "qwerty12" or password == "11111111":
            raise forms.ValidationError("Password is too common")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if password != reset_password:
            raise forms.ValidationError("Passwords do not match")
        return reset_password