from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, get_next_question, save_answers
from . import views

# Define the REST framework router
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

# Define core/general routes
core_patterns = [
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.update_settings, name='settings'),
]

# Define job-related routes
job_patterns = [
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_details, name='job_details'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('apply/', views.apply_job, name='apply_job'),
    path('', views.job_list, name='job_list'),  # For job listings
]

# Define interview-related routes
interview_patterns = [
    path('create/', views.interview_create, name='interview_create'),
    path('<int:pk>/', views.interview_detail, name='interview_detail'),
    path('<int:pk>/feedback/', views.interview_feedback, name='interview_feedback'),
    path('<int:interview_id>/questions/', views.fetch_questions, name='fetch_questions'),
    path('<int:interview_id>/submit_response/', views.submit_response, name='submit_response'),
    path('<int:interview_id>/next_question/', get_next_question, name='get_next_question'),
    path('<int:interview_id>/save_answers/', save_answers, name='save_answers'),
    path('schedule/', views.interview_schedule, name='interview_schedule'),
    path('', views.interview_list, name='interview_list'),
    path('complete/', views.interview_complete, name='interview_complete'),
]

# Define dashboard-related routes
dashboard_patterns = [
    path('candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('employer/', views.employer_dashboard, name='employer_dashboard'),
]

# Define candidate and employer management routes
management_patterns = [
    path('candidate/create/', views.candidate_create, name='candidate_create'),
    path('candidate/list/', views.candidate_list, name='candidate_list'),
    path('candidate/add/', views.add_candidate, name='add_candidate'),
    path('employer/add/', views.add_interview, name='add_interview'),  # Unclear - rename if specific
]

# Define skill assessment routes
skill_patterns = [
    path('', views.skill_assessment_list, name='skill_assessment_list'),
    path('create/', views.skill_assessment_create, name='skill_assessment_create'),
    path('<int:pk>/', views.skill_assessment_detail, name='skill_assessment_detail'),
    path('<int:pk>/result/', views.skill_assessment_result, name='skill_assessment_result'),
    path('<int:pk>/take/', views.skill_assessment_take, name='skill_assessment_take'),
]

# Combine all patterns in urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),  # API routes
    path('core/', include((core_patterns, 'core'))),
    path('jobs/', include((job_patterns, 'jobs'))),
    path('interviews/', include((interview_patterns, 'interviews'))),
    path('dashboard/', include((dashboard_patterns, 'dashboard'))),
    path('management/', include((management_patterns, 'management'))),
    path('skills/', include((skill_patterns, 'skills'))),
]

# Serve static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
