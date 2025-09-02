from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)


CATEGORY_CHOICES = [
    ('Technology & Innovation', 'Technology & Innovation'),
    ('Creative Arts', 'Creative Arts'),
    ('Food & Hospitality', 'Food & Hospitality'),
    ('Social Causes & Charity', 'Social Causes & Charity'),
    ('Education & Learning', 'Education & Learning'),
    ('Business & Entrepreneurship', 'Business & Entrepreneurship'),
    ('Travel & Adventure', 'Travel & Adventure'),
    ('Fashion & Design', 'Fashion & Design'),
    ('Sports & Athletics', 'Sports & Athletics'),
    ('Health & Wellness', 'Health & Wellness'),
]
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    total_target = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    is_reported = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError({
                'end_time': 'End time must be after start time.'
            })
        
        if self.start_time < timezone.now():
            raise ValidationError({
                'start_time': 'Start time cannot be in the past.'
            })
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(r.value for r in ratings) / ratings.count()
        return None
    
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)

class Reply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)


class Donation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=12, decimal_places=2,validators=[MinValueValidator(1)])  
    created_at = models.DateTimeField(auto_now_add=True)