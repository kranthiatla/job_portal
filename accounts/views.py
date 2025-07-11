from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RecruiterSignUpForm, JobSeekerSignUpForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
from accounts.tasks import send_welcome_email

# from accounts.views import CustomLogoutView



def recruiter_register(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_welcome_email.delay(user.email, user.username)
            return redirect('dashboard')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'Recruiter'})

def jobseeker_register(request):
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'Job Seeker'})



@login_required
def dashboard(request):
    if request.user.is_recruiter:
        return render(request, 'accounts/recruiter_dashboard.html')
    elif request.user.is_jobseeker:
        return render(request, 'accounts/jobseeker_dashboard.html')
    else:
        return redirect('login')




@csrf_exempt
def user_list_api(request):
    if request.method == 'GET':
        users = list(CustomUser.objects.values('id', 'username', 'email'))
        return JsonResponse(users, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')  # recruiter or jobseeker

            if not all([username, email, password, role]):
                return JsonResponse({'error': 'Missing fields'}, status=400)

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            user = CustomUser(
                username=username,
                email=email,
                password=make_password(password),
                is_recruiter=(role == 'recruiter'),
                is_jobseeker=(role == 'jobseeker'),
            )
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET and POST methods allowed'}, status=405)

@login_required
def recruiter_list(request):
    recruiters = CustomUser.objects.filter(is_recruiter=True)
    return render(request, 'accounts/recruiter_list.html', {'recruiters': recruiters})

@login_required
def jobseeker_list(request):
    jobseekers = CustomUser.objects.filter(is_jobseeker=True)
    return render(request, 'accounts/jobseeker_list.html', {'jobseekers': jobseekers})

@login_required
def dashboard(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'role': 'Recruiter' if user.is_recruiter else 'Job Seeker'
    }

    if user.is_recruiter:
        return render(request, 'accounts/recruiter_dashboard.html', context)
    elif user.is_jobseeker:
        return render(request, 'accounts/jobseeker_dashboard.html', context)
    else:
        return redirect('login')

# def recruiter_register(request):
#     ...
#     if form.is_valid():
#         user = form.save()
#         login(request, user)
#         send_welcome_email.delay(user.username)  # 🔁 background task
#         return redirect('dashboard')
