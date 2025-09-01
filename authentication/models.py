from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email_regex = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    message="Enter a valid email address.")
    email = models.EmailField(unique=True,validators=[email_regex])
    phone_regex = RegexValidator(
        regex=r'^(010|011|012|015)\d{8}$',
        message="Phone number must be a valid Egyptian number (11 digits)."
    )
    mobile = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

