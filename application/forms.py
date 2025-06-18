from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    Profile,
    Job,
    JobApplication,  # Replaces Application
    Interview,
    InterviewQuestion,
    InterviewResponse,  # Replaces InterviewAnswer
    SkillAssessment,
    AssessmentQuestion,
    AssessmentResult,  # Replaces SkillAssessmentResult
    CustomUser
)
from django.core.exceptions import ValidationError

class SentimentAnalysisForm(forms.Form):
    ANALYSIS_CHOICES = [
        ("cv", "Analyze CV"),
        ("interview", "Analyze Interview Answer"),
    ]

    analysis_type = forms.ChoiceField(choices=ANALYSIS_CHOICES, widget=forms.RadioSelect, required=True)
    interview_question = forms.CharField(max_length=500, required=False, 
                                       widget=forms.TextInput(attrs={'placeholder': 'Enter Interview Question'}))
    interview_answer = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Your Answer'}), required=False)
    resume = forms.FileField(required=False)

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

class InterviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = InterviewResponse
        fields = ['answer', 'interview', 'question']  # Using 'answer' instead of 'response_text'

from django import forms
from .models import Interview, InterviewResponse

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'title', 
            'description', 
            'candidate',  # ForeignKey to CustomUser
            'interviewer',  # ForeignKey to CustomUser
            'job',  # ForeignKey to Job (optional)
            'scheduled_time',  # DateTimeField
            'duration',  # PositiveIntegerField
            'question_set',  # CharField with choices
            'status'  # CharField with choices
        ]
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.NumberInput(attrs={'min': 15, 'max': 120}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class InterviewResponseForm(forms.ModelForm):
    class Meta:
        model = InterviewResponse
        fields = [
            'interview',  # ForeignKey to Interview
            'question',  # ForeignKey to InterviewQuestion
            'answer',  # TextField
            'score'  # PositiveIntegerField (optional)
        ]
        widgets = {
            'answer': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'score': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example of customizing querysets if needed
        if 'interview' in self.initial:
            self.fields['question'].queryset = InterviewQuestion.objects.filter(
                question_set=self.initial['interview'].question_set
            )

class InterviewScheduleForm(forms.Form):
    interview_date = forms.DateField(widget=forms.SelectDateWidget)
    interview_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

class SettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'bio', 'linkedin', 'github']

class SkillForm(forms.ModelForm):
    class Meta:
        model = SkillAssessment
        fields = ['name', 'description', 'passing_score']

class TakeSkillAssessmentForm(forms.ModelForm):
    class Meta:
        model = AssessmentResult
        fields = ['answers']

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    user_type_choices = [
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    ]
    user_type = forms.ChoiceField(choices=user_type_choices, required=True)
    phone = forms.CharField(max_length=20, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    linkedin = forms.URLField(required=False)
    github = forms.URLField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'bio', 'linkedin', 'github', 'user_type', 'password1', 'password2']

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'occupation', 'date_of_birth', 'industry',
            'currently_employed', 'current_company', 'company_name',
            'company_start_date', 'company_size', 'company_industry'
        ]

class JobApplicationForm(forms.ModelForm):
    candidate_name = forms.CharField(max_length=255, required=False, disabled=True)
    candidate_email = forms.EmailField(required=False, disabled=True)

    class Meta:
        model = JobApplication
        fields = ['job', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.candidate:
            self.fields['candidate_name'].initial = self.instance.candidate.username
            self.fields['candidate_email'].initial = self.instance.candidate.email

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = CustomUser  # Use your existing CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'occupation', 'date_of_birth', 'industry', 
                 'currently_employed', 'current_company', 'company_name',
                 'company_start_date', 'company_size', 'company_industry']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    user_type = forms.ChoiceField(choices=[('candidate', 'Candidate'), ('employer', 'Employer')])
    occupation = forms.CharField(required=False)
    candidate_industry = forms.CharField(required=False)
    company_name = forms.CharField(required=False)
    employer_industry = forms.CharField(required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'candidate':
            if not cleaned_data.get('occupation'):
                raise forms.ValidationError('Please enter your occupation.')
            if not cleaned_data.get('candidate_industry'):
                raise forms.ValidationError('Please enter your industry.')
        elif user_type == 'employer':
            if not cleaned_data.get('company_name'):
                raise forms.ValidationError('Please enter your company name.')
            if not cleaned_data.get('employer_industry'):
                raise forms.ValidationError('Please enter your employer industry.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                occupation=self.cleaned_data.get('occupation'),
                industry=self.cleaned_data.get('candidate_industry') or self.cleaned_data.get('employer_industry'),
                company_name=self.cleaned_data.get('company_name'),
                profile_picture=self.cleaned_data.get('photo')
            )
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'description', 
                 'experience', 'job_type', 'salary', 'deadline']