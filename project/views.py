from django.shortcuts import render,redirect
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request , "project/pages/home.html")

def profile(request):
    pass

def logout_view(request):
    logout(request)  
    return redirect('authentication:login')  