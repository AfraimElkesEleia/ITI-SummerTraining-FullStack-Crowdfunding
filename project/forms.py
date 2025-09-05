from django import forms
from .models import CustomUser, Profile,Project,TAG_CHOICES

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'profile_picture']
    def clean_email(self):
        return self.instance.email

class ProfileExtraForm(forms.ModelForm):
    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    facebook_profile = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    linkedin = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['birthdate', 'facebook_profile', 'linkedin', 'country']

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm your password",
        required=True
    )

class ProjectForm(forms.ModelForm):
     tags = forms.MultipleChoiceField(
        choices=TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple(),  # will render checkboxes
        required=False
    )
     class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'category',
            'tags',
            'image',
            'total_target',
            'start_time',
            'end_time'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your project'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'total_target': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total target in EGP'}),
            'start_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }