# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email") 
        password = request.POST.get("password")
        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("home") 
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "pages/login.html")

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our site.')
            return redirect('login')  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'pages/register.html', {'form': form})