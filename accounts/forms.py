from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RecruiterSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_recruiter = True
        if commit:
            user.save()
        return user

class JobSeekerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_jobseeker = True
        if commit:
            user.save()
        return user
