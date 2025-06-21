from django.utils import timezone
from django.contrib.auth import settings
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import phonenumbers
from phonenumbers import NumberParseException

from application.managers import CustomUserManager

# Constants for choices
class Choices:
    USER_TYPE = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )
    
    INTERVIEW_STATUS = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    
    QUESTION_SET = (
        ('problem_solving', 'Problem Solving'),
        ('decision_making', 'Decision Making'),
        ('technical_knowledge', 'Technical Knowledge'),
    )
    
    COMPANY_SIZE = (
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1001+', '1001+ employees'),
    )
    
    INDUSTRY = (
        ('tech', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        # ... other industries ...
    )
    
    JOB_TYPE = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )

# Validators
def validate_pdf(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError(_('Only PDF files are allowed.'))

def validate_phone(value):
    if not value:
        return
    try:
        parsed = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValidationError(_('Invalid phone number'))
    except NumberParseException:
        raise ValidationError(_('Invalid phone number format'))

# Abstract base models
class TimeStampedModel(models.Model):

    class Meta:
        abstract = True

# User-related models
class CustomUser(AbstractUser, TimeStampedModel):
    username = models.CharField(_('username'), max_length=255, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True, null=True, validators=[validate_phone])
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    bio = models.TextField(default="")  # or 'No bio provided'
    linkedin = models.URLField(default="https://www.linkedin.com/")
    github = models.URLField(default="https://github.com/")
    
    # Type flags
    user_type = models.CharField(_('user type'), max_length=20, choices=Choices.USER_TYPE, default='candidate')
    is_employer = models.BooleanField(_('is employer'), default=False)
    is_candidate = models.BooleanField(_('is candidate'), default=False)
    
    # Employer fields
    company_name = models.CharField(max_length=255, default="Unknown Company")
    industry = models.CharField(max_length=100, default="Not specified")
    company_size = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

# models.py
class CVUpload(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='cvs/', default='default_cv.pdf')
    parsed_text = models.TextField(blank=True)

    def __str__(self):
        return f"CV for {self.user.username}"

class Profile(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpeg')
    resume = models.FileField(_('resume'), upload_to='resumes/', blank=True, validators=[validate_pdf])
    
    # Common fields
    occupation = models.CharField(_('occupation'), max_length=100, blank=True)
    industry = models.CharField(_('industry'), max_length=100, choices=Choices.INDUSTRY, blank=True)
    experience = models.TextField(default="No experience provided")
    
    # Candidate-specific
    currently_employed = models.BooleanField(_('currently employed'), default=False)
    current_company = models.CharField(_('current company'), max_length=255, blank=True)
    
    # Employer-specific
    company_start_date = models.DateField(_('company start date'), blank=True, null=True)
    website = models.URLField(_('website'), blank=True)
    company_description = models.TextField(_('company description'), blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Job-related models
class Job(models.Model):
    title = models.CharField(_('title'), max_length=255)
    company_name = models.CharField(_('company name'), max_length=255)
    location = models.CharField(max_length=255, default="Not specified")
    description = models.TextField(_('description'))
    requirements = models.TextField(_('requirements'), blank=True)
    experience = models.PositiveIntegerField(_('years of experience'), default=0)
    job_type = models.CharField(_('job type'), max_length=20, choices=Choices.JOB_TYPE)
    salary = models.DecimalField(_('salary'), max_digits=10, decimal_places=2)
    deadline = models.DateField(_('application deadline'))
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('job')
        verbose_name_plural = _('jobs')

    def __str__(self):
        return f"{self.title} at {self.company_name}"

class JobApplication(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(_('resume'), upload_to='application_resumes/', validators=[validate_pdf])
    cover_letter = models.TextField(default="No cover letter provided")
    status = models.CharField(_('status'), max_length=20, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('job', 'candidate')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate}'s application for {self.job}"

# Interview-related models
class Interview(TimeStampedModel):
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interviews')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # <- Ensure this exists
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    interviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conducted_interviews')
    scheduled_time = models.DateTimeField(default=timezone.now)
    duration = models.PositiveIntegerField(_('duration (minutes)'), default=30)
    status = models.CharField(_('status'), max_length=20, choices=Choices.INTERVIEW_STATUS, default='scheduled')
    question_set = models.CharField(_('question set'), max_length=50, choices=Choices.QUESTION_SET)
    feedback = models.TextField(default="No feedback provided")

    class Meta:
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"Interview for {self.candidate} - {self.title}"

class InterviewQuestion(models.Model):
    question_set = models.CharField(max_length=255, default='Default Set')  # adjust as needed
    text = models.TextField(default='Placeholder question')  # or an actual default question
    order = models.PositiveIntegerField(_('order'))

    class Meta:
        ordering = ['question_set', 'order']
        unique_together = ('question_set', 'order')

    def __str__(self):
        return f"{self.get_question_set_display()} - Q{self.order}"

class InterviewResponse(TimeStampedModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, related_name='responses')
    answer = models.TextField(default="No response")
    score = models.PositiveIntegerField(_('score'), null=True, blank=True)

    class Meta:
        unique_together = ('interview', 'question')

    def __str__(self):
        return f"Response to {self.question} by {self.interview.candidate}"

# Skill assessment models
class SkillAssessment(TimeStampedModel):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    passing_score = models.PositiveIntegerField(_('passing score'), default=70)
    is_active = models.BooleanField(_('is active'), default=True)

    def __str__(self):
        return self.name

class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(SkillAssessment, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(_('question text'))
    order = models.PositiveIntegerField(_('order'))
    correct_answer = models.TextField(_('correct answer'), blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ('assessment', 'order')

    def __str__(self):
        return f"Q{self.order} for {self.assessment}"

class AssessmentResult(models.Model):
    assessment = models.ForeignKey(SkillAssessment, on_delete=models.CASCADE, related_name='results')
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assessment_results')
    score = models.DecimalField(_('score'), max_digits=5, decimal_places=2)
    passed = models.BooleanField(_('passed'), default=False)
    details = models.JSONField(_('details'), default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('assessment', 'candidate')

    def save(self, *args, **kwargs):
        self.passed = self.score >= self.assessment.passing_score
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate}'s result for {self.assessment}"

# Signals
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)