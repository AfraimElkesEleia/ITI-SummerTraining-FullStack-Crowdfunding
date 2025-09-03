from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from .forms import UserProfileForm, ProfileExtraForm,DeleteAccountForm,ProjectForm
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Avg,Sum,Count
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
# Create your views here.
TAG_CHOICES = [
    "Tech",
    "Health",
    "Education",
    "Art",
    "Food",
    "Business",
    "Travel",
    "Fashion",
    "Sports",
    "Social",
    "AI",
    "Flutter",
    "Computer Vision",
]

CATEGORY_CHOICES = [
    "Technology & Innovation",
    "Creative Arts",
    "Food & Hospitality",
    "Social Causes & Charity",
    "Education & Learning",
    "Business & Entrepreneurship",
    "Travel & Adventure",
    "Fashion & Design",
    "Sports & Athletics",
    "Health & Wellness",
]

def home(request):
    active_projects = Project.objects.filter(is_canceled=False)
    latest_projects = active_projects.order_by('-created_at')[:5]
    top_rated = sorted(active_projects, key=lambda p: p.average_rating(), reverse=True)[:5]
    
    context = {
        'top_rated': top_rated,
        'latest_projects': latest_projects,
        'categories': CATEGORY_CHOICES,  
    }
    return render(request, 'project/pages/home.html', context)
def logout_view(request):
    logout(request)  
    return redirect('authentication:login')  
def show_profile(request,user_id):
    profile = Profile.objects.get(user_id = user_id)
    return render(request , 'project/pages/profile.html' , {'profile':profile})
def edit_profile(request,id):
    user = CustomUser.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        profile_form = ProfileExtraForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully ✅")
        else:
            messages.error(request, "Please correct the errors below ❌")
        return redirect('home')
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileExtraForm(instance=profile)

    return render(request, "project/pages/edit_profile.html", {
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
@csrf_exempt
def project_details(request,id):
    current_project = Project.objects.get(id=id)
    user_rating = None
    try:
        user_rating = Rating.objects.get(project=current_project, user=request.user).value
    except Rating.DoesNotExist:
        user_rating = 0
    donation_stats = current_project.donations.aggregate(
        total_raised=Sum('amount'),
        supporters=Count('user', distinct=True)
    )
    total_raised = donation_stats['total_raised'] or 0
    supporters = donation_stats['supporters'] or 0
    progress_percentage = 0
    if current_project.total_target > 0:
        progress_percentage = round(float(total_raised) / float(current_project.total_target) * 100, 2)
    if request.method == 'POST' and not current_project.is_canceled:
        data = json.loads(request.body)
        text = data.get('comment_text')
        if text:
            comment = Comment.objects.create(user=request.user, project=current_project, text=text)
            profile_url = None
            if bool(comment.user.profile_picture):
                profile_url = comment.user.profile_picture.url
            else:
                profile_url = '/static/images/no_profile.png'
            print(profile_url)
            return JsonResponse({
                'id': comment.id,
                'user': f"{comment.user.first_name} {comment.user.last_name}",
                'text': comment.text,
                'created_at': comment.created_at.strftime("%b %d, %Y %H:%M"),
            })
    comments = current_project.comments.all().order_by('-created_at')
    def get_tags_list(tags_string):
        return [t.strip().lower() for t in tags_string.split(",") if t.strip()]

    project_tags = get_tags_list(current_project.tags or "")
    all_projects = Project.objects.filter(is_canceled=False).exclude(id=current_project.id)

    similar_projects = []
    for p in all_projects:
        other_tags = get_tags_list(p.tags or "")
        common = set(project_tags) & set(other_tags)  
        if common:
            similar_projects.append((p, len(common)))
    similar_projects = [p for p, _ in sorted(similar_projects, key=lambda x: x[1], reverse=True)[:4]]
    context = {
        'project': current_project,
        'comments':comments,
        'user_rating': user_rating,
        'current_total': total_raised,
        'donors_count': supporters,
        'progress_percentage':progress_percentage,
        'similar_projects':similar_projects
    }
    return render(request,"project/pages/project_details.html",context)
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
        print("Raw tags from DB:", project)
        tags = project.tags.split(",") if project.tags else []
        print( project.tags)
        tags = [tag.strip() for tag in tags] 
        return JsonResponse({"tags": tags})
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)
    
@csrf_exempt
@login_required
def donate_project(request, project_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount', 0))
            project = Project.objects.get(id=project_id)
            if(project.is_canceled):
               return JsonResponse({'success': False, 'message': 'You cannot donate to this project' })
            user = request.user
            current_total = project.donations.aggregate(total= Sum('amount'))['total'] or 0
            if current_total + amount > project.total_target:
                return JsonResponse({
                    'success': False,
                    'message': 'Donation exceeds project target!'
                })

            Donation.objects.create(project=project, user=user, amount=amount)
            current_total = project.donations.aggregate(total=Sum('amount'))['total'] or 0
            donors_count = project.donations.values('user').distinct().count()
            return JsonResponse({
                'success': True,
                'current_total': float(current_total),
                'donors_count': donors_count
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
@csrf_exempt
@login_required
def cancel_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.user != project.owner:
        return JsonResponse({'error': "You are not allowed to cancel this project."}, status=400)
    current_total = Donation.objects.filter(project=project).aggregate(total=Sum('amount'))['total'] or 0
    progress_percentage = 0
    if project.total_target > 0:
        progress_percentage = round((current_total / project.total_target) * 100)
    if progress_percentage >= 25:
        return JsonResponse({'error': 'Cannot cancel project after reaching 25% funding.'}, status=400)
    project.is_canceled = True
    project.save()
    print("cancelled done")
    return JsonResponse({'success': True, 'message': 'Project has been canceled.'})

@csrf_exempt
def reply(request,comment_id):
    comment = Comment.objects.get(id=comment_id)
    data = json.loads(request.body)
    text = data.get('reply_text')
    if text:
        reply = Reply.objects.create(user=request.user, comment=comment, text=text)
        return JsonResponse({
            'success': True,
            'user': f"{reply.user.first_name} {reply.user.last_name}",
            'text': reply.text,
            'created_at': reply.created_at.strftime("%b %d, %Y %H:%M"),
        })
    return JsonResponse({'success': False})

def category_projects(request, category):
    category_names = CATEGORY_CHOICES
    if category not in category_names:
        return render(request, 'project/pages/category_projects.html', {
            'error': 'Category not found',
            'projects': [],
            'category': category
        })

    projects = Project.objects.filter(category=category)
    context = {
        'projects': projects,
        'category': category
    }
    return render(request, 'project/pages/category_projects.html', context)

def all_projects(request):
    all_projects = Project.objects.all()
    return render(request,'project/pages/all_projects.html',{'projects':all_projects})

@login_required
def my_donations(request,user_id):
    current_user = CustomUser.objects.get(id=user_id)
    donations = Donation.objects.filter(user=current_user).order_by('-created_at')
    
    context = {
        'donations': donations
    }
    return render(request, 'project/pages/my_donations.html', context)