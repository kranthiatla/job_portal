from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),

]
