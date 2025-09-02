# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string  
from django.contrib.sites.shortcuts import get_current_site
from .models import CustomUser
from project.models import Profile
from .tokens import account_activation_token
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email") 
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:  
                login(request, user)
                return redirect("home")
            else:
                messages.warning(request, "Your account is not activated. Please check your email.")
                return redirect('authentication:login')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "pages/login.html")

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
                user = form.save(commit=False)
                user.is_active=False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('authentication:login')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('authentication:login')   

def activateEmail(request, user, to_email):
    mail_subject = "Activate user account."
    message = render_to_string("email_activation.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.first_name} {user.last_name}, please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
