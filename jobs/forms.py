from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['posted_by']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
