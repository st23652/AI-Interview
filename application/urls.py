from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .cv_parser.cv_parser import upload_files
from .views import get_next_question, save_answers, analyze_page, analyze_cv, analyze_interview
from rest_framework.routers import SimpleRouter
from application.views import ai_interview, ai_feedback

# Define the router and register your viewsets
router = SimpleRouter()
router.register(r'users', views.JobViewSet)

# Define your URL patterns
urlpatterns = [
    path('process_image/', views.process_image, name='process_image'),
    path("api/interview/", ai_interview, name="ai_interview"),
    path("api/feedback/", ai_feedback, name="ai_feedback"),
    path('api/', include(router.urls)),  # Add prefix to avoid collision with other paths
    path('home/', views.home, name='home'),  # Adjusted 'home' path to prevent recursion
    path('analyze/', analyze_page, name='analyze_page'),
    path('analyze/cv/', analyze_cv, name='analyze_cv'),
    path('analyze/interview/', analyze_interview, name='analyze_interview'),
    path('upload/', upload_files, name='upload_files'),
    path('candidate/home/', views.candidate_home, name='candidate_home'),
    path('employer/home/', views.employer_home, name='employer_home'),
    path('interview/questions/', views.fetch_questions, name='fetch_questions'),
    path('interview/submit_response/', views.submit_response, name='submit_response'),
    path('api/interview/<int:interview_id>/questions/', views.get_interview_questions, name='get_interview_questions'),
    path('interview/next_question/<int:interview_id>/', views.get_next_question, name='get_next_question'),    path('interview/save_answers/', save_answers, name='save_answers'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('register/', views.register_view, name='register_view'),
    path('auto-interview/', views.auto_interview, name='auto_interview'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/', views.job_details, name='job_details'),  # Corrected from 'job_detail' to 'job_details'
    path('job/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('apply_job/', views.apply_job, name='apply_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('interview/create/', views.interview_create, name='interview_create'),
    path('interview/<int:pk>/', views.interview_detail, name='interview_detail'),
    path('interview/<int:pk>/feedback/', views.interview_feedback, name='interview_feedback'),
    path('interview/', views.interview, name='interview'),
    path('interview/list', views.interview_list, name='interview_list'),
    path('interview/<int:sector_id>/', views.interview_detail, name='interview_detail'),
    path('complete/', views.interview_complete, name='interview_complete'),
    path('candidate/create/', views.candidate_create, name='candidate_create'),
    path('add_candidate/', views.add_candidate, name='add_candidate'),
    path('add_interview/', views.add_interview, name='add_interview'),
    path('add_job/', views.add_job, name='add_job'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('interview_schedule/', views.interview_schedule, name='interview_schedule'),
    path('interview/', views.interview, name='interview'),
    path('job_application_list/', views.job_application_list, name='job_application_list'),
    path('job_postings/', views.job_postings, name='job_postings'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('settings/', views.update_settings, name='settings'),
    path('skills/', views.skill_assessment_list, name='skill_assessment_list'),
    path('skills/create/', views.skill_assessment_create, name='skill_assessment_create'),
    path('skills/<int:pk>/', views.skill_assessment_detail, name='skill_assessment_detail'),
    path('skills/<int:pk>/result/', views.skill_assessment_result, name='skill_assessment_result'),
    path('skills/<int:pk>/take/', views.skill_assessment_take, name='skill_assessment_take'),
    path('upload/', views.upload_resume, name='upload'),
]

# Append router URLs to the urlpatterns
urlpatterns += router.urls

# Add static URL handling in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
