from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import UserProfileForm, ProfileExtraForm
from .models import Profile,CustomUser
# Create your views here.
def home(request):
    return render(request , "project/pages/home.html")

def logout_view(request):
    logout(request)  
    return redirect('authentication:login')  

def edit_profile(request,id):
    user = CustomUser.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        profile_form = ProfileExtraForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("home")  

    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileExtraForm(instance=profile)

    return render(request, "project/pages/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })