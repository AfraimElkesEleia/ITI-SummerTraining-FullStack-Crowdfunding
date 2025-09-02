from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from .forms import UserProfileForm, ProfileExtraForm,DeleteAccountForm,ProjectForm
from .models import Profile,CustomUser,Project
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    latest_projects = Project.objects.all().order_by('-created_at')[:5]
    all_projects = Project.objects.all()
    top_rated = sorted(all_projects, key=lambda p: p.average_rating(), reverse=True)[:5]
    context = {
        'top_rated': top_rated,
        'latest_projects': latest_projects,
        'all_projects': all_projects,
    }
    return render(request, 'project/pages/home.html', context)

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

def delete_account(request, id):
    if request.method == "POST":
        form = DeleteAccountForm(request.POST)
        user = CustomUser.objects.get(id=id)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = authenticate(email= user.email, password= password)
            if user is not None:
                request.user.delete()
                logout(request)
                messages.success(request, "Your account has been deleted successfully.")
                return redirect("authentication:login")
            else:
                messages.error(request, "Incorrect password. Please try again.")
    else:
        form = DeleteAccountForm()

    return render(request, "project/pages/delete_account.html", {"form": form})

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.tags = ','.join(form.cleaned_data['tags'])
            project.save()
            messages.success(request, "Project created successfully!")
            return redirect("home")  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm()

    return render(request, "project/pages/create_project.html", {"form": form})