# Define the router and register your viewsets
import stat
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from myproject import settings
from . import views

from application.views import ai_feedback, ai_interview
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# Note: You registered JobViewSet with 'users'. This might be a typo. Let's assume you meant 'jobs'.
router.register(r'jobs', views.JobViewSet) 
router.register(r'users', views.CustomUserViewSet)
router.register(r'interviews', views.InterviewViewSet)

# Define your URL patterns
urlpatterns = [
    # API URLs
    path('api/', include(router.urls)), # Include router URLs once
    path("api/interview/", ai_interview, name="ai_interview"),
    path("api/feedback/", ai_feedback, name="ai_feedback"),
    path('api/interview/<int:interview_id>/questions/', views.get_interview_questions, name='get_interview_questions'),

    # Main pages
    path('home/', views.home, name='home'),
    path('candidate/home/', views.candidate_home, name='candidate_home'),
    path('employer/home/', views.employer_home, name='employer_home'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),

    # Auth
    path('register/', views.register_view, name='register_view'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # Profile & Settings
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('settings/', views.update_settings, name='settings'),

    # Job and Application
    path('jobs/', views.job_list, name='job_list'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/', views.job_details, name='job_details'),
    path('job/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'), # Assumes apply_job needs pk

    # Interview
    path('interview/create/', views.interview_create, name='interview_create'),
    path('interviews/', views.InterviewListView.as_view(), name='interview_list'),
    path('interview/<int:pk>/', views.InterviewDetailView.as_view(), name='interview_detail'),
    path('interview/<int:pk>/feedback/', views.interview_feedback, name='interview_feedback'),
    path('interview/schedule/', views.interview_schedule, name='interview_schedule'),
    path('interview/complete/', views.interview_complete, name='interview_complete'),
    path('interview/start/', views.interview, name='start_interview'), # Renamed for clarity

    # Skill Assessment
    path('skills/', views.skill_assessment_list, name='skill_assessment_list'),
    path('skills/create/', views.skill_assessment_create, name='skill_assessment_create'),
    path('skills/<int:pk>/', views.skill_assessment_detail, name='skill_assessment_detail'),
    path('skills/<int:pk>/take/', views.skill_assessment_take, name='skill_assessment_take'),
    path('skills/<int:pk>/result/', views.skill_assessment_result, name='skill_assessment_result'),

    # Other
    # ... other unique paths
]
