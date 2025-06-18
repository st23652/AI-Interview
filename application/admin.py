from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Profile,
    Job,
    JobApplication,
    Interview,
    InterviewQuestion,
    InterviewResponse,
    SkillAssessment,
    AssessmentQuestion,
    AssessmentResult
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_employer', 'is_candidate', 'company_name', 'industry')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_employer', 'is_candidate', 'company_name', 'industry',
                         'phone', 'date_of_birth', 'bio', 'linkedin', 'github')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'occupation', 'industry', 'currently_employed')
    search_fields = ('user__username', 'occupation')
    list_filter = ('industry', 'currently_employed')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'job_type', 'location', 'deadline', 'is_active')
    search_fields = ('title', 'company_name', 'description')
    list_filter = ('job_type', 'location', 'is_active')
    ordering = ('-created_at',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'candidate', 'status', 'created_at')
    search_fields = ('job__title', 'candidate__username')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'interviewer', 'scheduled_time', 'status')
    search_fields = ('candidate__username', 'job__title', 'interviewer__username')
    list_filter = ('status', 'question_set')
    ordering = ('-scheduled_time',)

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_set', 'text', 'order')
    search_fields = ('text',)
    list_filter = ('question_set',)
    ordering = ('question_set', 'order')

@admin.register(InterviewResponse)
class InterviewResponseAdmin(admin.ModelAdmin):
    list_display = ('interview', 'question', 'score')
    search_fields = ('interview__candidate__username', 'question__text')
    list_filter = ('interview',)

@admin.register(SkillAssessment)
class SkillAssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'passing_score', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'text', 'order')
    search_fields = ('text',)
    list_filter = ('assessment',)
    ordering = ('assessment', 'order')

@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'candidate', 'score', 'passed', 'created_at')
    search_fields = ('assessment__name', 'candidate__username')
    list_filter = ('passed', 'created_at')
    ordering = ('-created_at',)