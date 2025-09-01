from django.db import models
from authentication.models import CustomUser

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
