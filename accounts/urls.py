# from django.urls import path
# from  accounts.views import  user_list_api, recruiter_register, jobseeker_register
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('recruiter/register/', recruiter_register, name='recruiter_register'),
#     path('jobseeker/register/', jobseeker_register, name='jobseeker_register'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('api/users/', user_list_api, name='user_list_api'),
# ]

from accounts import views as accounts_views
from django.urls import path
from . import views


urlpatterns = [
    path('accounts/register/recruiter/', views.recruiter_register, name='recruiter_register'),
    path('accounts/register/jobseeker/', views.jobseeker_register, name='jobseeker_register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recruiters/', views.recruiter_list, name='recruiter_list'),
    path('jobseekers/', views.jobseeker_list, name='jobseeker_list'),
    path('accounts/dashboard/', accounts_views.dashboard, name='dashboard'),
    path('api/users/', accounts_views.user_list_api, name='user_api'),
]


