from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job,Application
from .forms import JobForm, ApplicationForm
from django.contrib import messages

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.user.is_recruiter:
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.posted_by = request.user
                job.save()
                return redirect('job_list')
        else:
            form = JobForm()
        return render(request, 'jobs/post_job.html', {'form': form})
    return redirect('job_list')

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f'You have successfully applied to {job.title}!')
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def recruiter_dashboard(request):
    if not request.user.is_recruiter:
        return redirect('job_list')

    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__in=jobs)

    return render(request, 'jobs/recruiter_dashboard.html', {
        'jobs': jobs,
        'applications': applications
    })

from django.shortcuts import render
from .models import Job

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
