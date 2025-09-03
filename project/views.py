from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from .forms import UserProfileForm, ProfileExtraForm,DeleteAccountForm,ProjectForm
from .models import Profile,CustomUser,Project,Rating
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
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

def project_details(request,id):
    current_project = Project.objects.get(id=id)
    user_rating = None
    try:
        user_rating = Rating.objects.get(project=current_project, user=request.user).value
    except Rating.DoesNotExist:
        user_rating = 0
    return render(request,"project/pages/project_details.html",{'project':current_project,'user_rating':user_rating})
@csrf_exempt
def rate_project(request, project_id, user_id):
    if request.method == "POST":
        print('inside rate view')
        data = json.loads(request.body)  
        rating_value = int(data.get('rating'))
        print(rating_value)
        project = Project.objects.get(id=project_id)
        user = CustomUser.objects.get(id=user_id)
        existing_rating = Rating.objects.filter(project=project, user=user).first()
        if existing_rating:
            existing_rating.value = rating_value
            existing_rating.save()
        else:
            Rating.objects.create(project=project, user=user, value=rating_value)
        ratings = Rating.objects.filter(project=project)
        total_ratings = ratings.count()
        average_rating = ratings.aggregate(avg=Avg('value'))['avg'] or 0
        return JsonResponse({
            'success': True,
            'average_rating': round(average_rating, 1),
            'total_ratings': total_ratings
        })
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
def get_project_tags(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        tags = project.tags.split(",") if project.tags else []
        tags = [tag.strip() for tag in tags]  # remove spaces
        return JsonResponse({"tags": tags})
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)