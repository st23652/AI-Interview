from asyncio.log import logger
from PyPDF2 import PdfReader
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import openai
from docx2txt import docx2txt
from . import models
from .forms import CandidateProfileForm, JobApplicationForm, JobForm, ProfileForm, SettingsForm, \
    InterviewScheduleForm, CustomUserCreationForm, InterviewForm, SkillAssessmentForm, UserRegistrationForm, YourForm
from .forms import AnswerForm
from .models import InterviewResponse, Candidate, Job, SkillAssessment
import json
from .forms import ProfilePictureForm
from django.views.decorators.csrf import csrf_exempt
from openai import ChatCompletion
from django.template.loader import render_to_string
import spacy
from pdfminer.high_level import extract_text
from .forms import CVUploadForm
from spacy.matcher import Matcher
from rest_framework import viewsets
from .serializers import InterviewSerializer, JobSerializer, CustomUserSerializer
from .forms import InterviewFeedbackForm
import os
from dotenv import load_dotenv
from application.ai_feedback.analyzers import InternalSentimentAnalyzer
from .forms import SentimentAnalysisForm
from .forms import EmailAuthenticationForm  # Import the custom form
from .utils import generate_interview_question, evaluate_answer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import detect_face_and_emotion
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# ======================================================
# NEWLY ADDED IMPORTS
# ======================================================
from django.contrib.auth.models import Group

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Save the new user

            # ======================================================
            # NEWLY ADDED CODE
            # ======================================================
            # Find the 'Recruiters' group we created in the admin panel.
            try:
                recruiters_group = Group.objects.get(name='Recruiters')
                # Add the new user to this group.
                user.groups.add(recruiters_group)
            except Group.DoesNotExist:
                # Handle case where group doesn't exist yet, though it shouldn't happen
                # if you completed Step 1.
                pass
            # ======================================================

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'templates/register.html', context)

@csrf_exempt
def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        result = detect_face_and_emotion(image)
        return JsonResponse(result)
    return JsonResponse({"error": "No image provided"}, status=400)

# OopCompanion:suppressRename

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@csrf_exempt
def ai_interview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        job_role = data.get("job_role", "Software Engineer")
        previous_answer = data.get("previous_answer", "")

        next_question = generate_interview_question(job_role, previous_answer)

        return JsonResponse({"question": next_question})

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def ai_feedback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        job_role = data.get("job_role", "Software Engineer")
        question = data.get("question", "")
        candidate_answer = data.get("candidate_answer", "")

        feedback = evaluate_answer(job_role, question, candidate_answer)

        return JsonResponse({"feedback": feedback})

    return JsonResponse({"error": "Invalid request"}, status=400)

def analyze_page(request):
    return render(request, 'analyze.html')

def analyze_cv(request):
    return render(request, 'analyze_cv.html')

def analyze_interview(request):
    return render(request, 'analyze_interview.html')

def extract_text_from_file(file_path):
    """Extracts text from PDF or DOCX files."""
    if file_path.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            return f"Error reading PDF: {e}"
    elif file_path.endswith(".docx"):
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            return f"Error reading DOCX: {e}"
    return "Unsupported file format"

def analyze_sentiment(request):
    """Handles sentiment analysis for CV or interview answer."""
    if request.method == "POST":
        form = SentimentAnalysisForm(request.POST, request.FILES)

        if form.is_valid():
            analysis_type = form.cleaned_data["analysis_type"]

            if analysis_type == "cv":
                cv_file = request.FILES.get("cv_file")
                if not cv_file:
                    return JsonResponse({"error": "Please upload a CV file."}, status=400)

                cv_path = os.path.join(UPLOAD_FOLDER, cv_file.name)
                default_storage.save(cv_path, ContentFile(cv_file.read()))
                cv_text = extract_text_from_file(cv_path)

                if "Error" in cv_text:
                    return JsonResponse({"error": cv_text}, status=500)

                analyzer = InternalSentimentAnalyzer()
                result = analyzer.analyze(cv_text)

                return JsonResponse({
                    "analysis_type": "CV",
                    "score": result["score"],
                    "sentiment": result["sentiment"],
                })

            elif analysis_type == "interview":
                question = form.cleaned_data["interview_question"]
                answer = form.cleaned_data["interview_answer"]

                if not question or not answer:
                    return JsonResponse({"error": "Please enter both question and answer."}, status=400)

                combined_text = f"Question: {question}\nAnswer: {answer}"
                analyzer = InternalSentimentAnalyzer()
                result = analyzer.analyze(combined_text)

                return JsonResponse({
                    "analysis_type": "Interview Answer",
                    "score": result["score"],
                    "sentiment": result["sentiment"],
                })

    else:
        form = SentimentAnalysisForm()

    return render(request, "analyze.html", {"form": form})

load_dotenv()

def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Now username is actually email
            password = form.cleaned_data.get('password')

            # Authenticate the user using email
            user = authenticate(request, username=email, password=password)  # username=email is required

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or another page
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def fetch_questions(request, interview_id):
    interview = models.Interview.objects.get(id=interview_id)
    questions = models.InterviewQuestion.objects.filter(interview=interview).order_by('order')

    # Return question data as JSON
    questions_data = [{'id': q.id, 'text': q.question_text} for q in questions]
    return JsonResponse({'questions': questions_data})

@csrf_exempt
def submit_response(request, interview_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        interview = models.Interview.objects.get(id=interview_id)
        question = models.InterviewQuestion.objects.get(id=data['question'])

        # Save the response
        response = InterviewResponse.objects.create(
            interview=interview,
            question=question,
            answer=data['response']
        )
        return JsonResponse({'status': 'success'})

def interview_feedback(request, interview_id):
    interview = get_object_or_404(models.Interview, id=interview_id)

    if request.method == 'POST':
        form = InterviewFeedbackForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('interview_detail',
                            interview_id=interview.id)  # Redirect to the interview detail page or any other page
    else:
        form = InterviewFeedbackForm(instance=interview)

    return render(request, 'interview_feedback.html', {'form': form, 'interview': interview})

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()  # Get all users
    serializer_class = CustomUserSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = JobSerializer

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = models.Interview.objects.all()
    serializer_class = InterviewSerializer

@login_required
def dashboard_redirect(request):
    if request.user.is_candidate:
        return redirect('candidate_dashboard')
    elif request.user.is_employer:
        return redirect('employer_dashboard')
    else:
        return redirect('default_dashboard')

def candidate_dashboard(request):
    # Example data, typically you'd fetch this from a database
    jobs = [
        {
            'title': 'Job X',
            'applied_date': '01/01/2024',
            'interview_date': '15/01/2024',
            'reviewed_date': '20/01/2024'
        },
        {
            'title': 'Job Y',
            'applied_date': '02/01/2024',
            'interview_date': '18/01/2024',
            'reviewed_date': '22/01/2024'
        }
    ]

    return render(request, 'candidate_dashboard.html', {'jobs': jobs})

@login_required
def employer_dashboard(request):
    # Employer-specific logic
    employer_jobs = [
        {
            'job_title': 'Job X',
            'candidates': [
                {'name': 'Candidate X', 'status': 'Applied'},
                {'name': 'Candidate Y', 'status': 'Interview Scheduled'},
                {'name': 'Candidate Z', 'status': 'Accepted'},
            ],
            'job_description': 'Detailed job description here.',
        },
    ]

    context = {
        'employer_jobs': employer_jobs,
    }

    return render(request, 'employer_dashboard.html', context)

@login_required
def dashboard(request):
    if request.user.is_employer:
        return render(request, 'employer_dashboard.html')
    elif request.user.is_candidate:
        return render(request, 'candidate_dashboard.html')
    return redirect('user_login')

def some_view(request):
    user = request.user
    context = {
        'is_employer': user.is_employer,  # Assuming you have a boolean field is_employer
        'is_candidate': user.is_candidate,  # Assuming you have a boolean field is_candidate
    }
    return render(request, 'your_template.html', context)

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

# Define custom patterns for matching specific resume information
skill_pattern = [{"POS": "NOUN", "OP": "+"}, {"LOWER": "experience"}]
matcher.add("EXPERIENCE", [skill_pattern])

def parse_resume_text(file_path):
    text = extract_text(file_path)
    return text

def extract_information(text):
    doc = nlp(text)
    skills = []
    experience = []
    education = []

    # Apply custom matcher patterns
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if nlp.vocab.strings[match_id] == "EXPERIENCE":
            experience.append(span.text)

    # Extract entities using spaCy's NER
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            experience.append(ent.text)
        elif ent.label_ == 'GPE':
            education.append(ent.text)

    return {
        'skills': ', '.join(set(skills)),
        'experience': ', '.join(set(experience)),
        'education': ', '.join(set(education)),
    }

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_resume(file):
    if file.size > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("File too large (max 5MB).")
    if not file.name.endswith(('.pdf', '.docx')):
        raise ValidationError("Only PDF/DOCX files allowed.")

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                validate_resume(request.FILES['file'])
                form.save()
                return redirect('resume_success')
            except ValidationError as e:
                messages.error(request, str(e))  # User feedback
    else:
        form = CVUploadForm()
    return render(request, 'upload_resume.html', {'form': form})

def auto_interview(request):
    return render(request, 'auto_interview.html')

interview_link = "http://127.0.0.1:8000/interviews/1/"
message = render_to_string('email_templates/interview_link_email.html', {
    'interview_link': interview_link,
    'recruiter_name': 'Recruiter',
})
print(message)

def create_interview(request):
    # Code to create an interview instance
    interview = models.Interview.objects.create(
        title="Sample Interview",
        description="Description",
        candidate_id=1,
        interviewer_id=2,
        scheduled_date="2024-08-17T10:00:00Z",
        status="Scheduled",
        question_set="Set1",
        answers={},
        completed=False
    )

    # Send email to recruiter
    send_interview_link(interview.id, 'recruiter@example.com')

    return HttpResponse("Interview created and email sent.")

# tasks.py (Celery task)
@shared_task(bind=True)
def send_interview_link_async(self, interview_id, recruiter_email):
    try:
        interview = models.Interview.objects.get(id=interview_id)
        send_mail(
            subject="Interview Scheduled",
            message=f"Link: http://example.com/interviews/{interview_id}/",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recruiter_email],
        )
    except Exception as e:
        logger.error(f"Email failed: {e}")
        self.retry(countdown=60)  # Retry after 60 seconds

# views.py
def send_interview_link(interview_id, recruiter_email):
    send_interview_link_async.delay(interview_id, recruiter_email)  # Non-blocking

def get_next_question(request, interview_id):
    try:
        interview = models.Interview.objects.get(id=interview_id)
        job = interview.job
        answers = json.loads(request.GET.get('answers', '{}'))

        next_question = generate_next_question(job, answers)
        return JsonResponse({'question': next_question})
    except models.Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found'}, status=404)

def generate_next_question(job, answers):
    # Example logic to generate the next question based on answers
    questions = models.InterviewQuestion.objects.filter(job=job).values_list('question', flat=True)

    if not answers:
        return questions[0] if questions else "No questions available."
    else:
        return questions[len(answers)] if len(answers) < len(questions) else "No more questions."

@login_required
def interview_create(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.user = request.user
            interview.save()

            # Generate AI-powered questions
            ai_questions = generate_ai_questions(interview.job_position)
            for question in ai_questions:
                models.InterviewQuestion.objects.create(
                    interview=interview,
                    question_text=question
                )

            return redirect('interview_list')

    else:
        form = InterviewForm()

    return render(request, 'interview_create.html', {'form': form})

from django.core.cache import cache
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))  # Retry 3 times on failure
def fetch_ai_questions(job_position):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": f"Generate 5 questions for {job_position}."}]
    )
    return [choice['message']['content'] for choice in response['choices']]

def generate_ai_questions(job_position):
    cache_key = f"ai_questions_{job_position}"
    if cached := cache.get(cache_key):
        return cached
    try:
        questions = fetch_ai_questions(job_position)
        cache.set(cache_key, questions, timeout=3600)  # Cache for 1 hour
        return questions
    except Exception as e:
        logger.error(f"OpenAI API failed: {e}")
        return ["Fallback question 1", "Fallback question 2"]  # Graceful degradation

def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to a page where you list jobs
        else:
            print(form.errors)
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})

@csrf_exempt
def save_answers(request, interview_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            interview = models.Interview.objects.get(id=interview_id)
            for question_text, answer in data.items():
                # Find the question object
                question = models.Question.objects.get(text=question_text)
                # Save the answer
                InterviewResponse.objects.create(interview=interview, question=question, answer=answer)
            return JsonResponse({'message': 'Responses saved successfully.'}, status=200)
        except models.Interview.DoesNotExist:
            return JsonResponse({'error': 'Interview not found.'}, status=404)
        except models.Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def profile(request):
    profile = request.user.profile  # Assuming the user has a one-to-one relationship with the Profile model

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'user': request.user})

def interview_questions(request, interview_id):
    interview = get_object_or_404(models.Interview, id=interview_id)
    if request.method == 'POST':
        # Assuming answers are submitted via POST request
        answers = request.POST.get('answers')
        interview.answers = answers
        interview.completed = True
        interview.save()
        return redirect('interview_complete', interview_id=interview.id)
    return render(request, 'interview.html', {'interview': interview})

def question_set(request, set_name):
    questions = models.Question.objects.filter(question_set=set_name)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.save()
            return redirect('interview_questions')
        else:
            print(form.errors)
    else:
        form = AnswerForm()
    return render(request, 'question_set.html', {'questions': questions, 'form': form})

def skill_assessment_detail(request, pk):
    assessment = get_object_or_404(models.SkillAssessment, pk=pk)
    context = {'assessment': assessment}
    return render(request, 'skill_assessment_detail.html', context)

@login_required
def edit_profile(request):
    try:
        user_profile = request.user.profile
    except models.Profile.DoesNotExist:
        user_profile = models.Profile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=user_profile)

    industry_choices = ProfileForm.industry_choices

    return render(request, 'edit_profile.html', {'form': form, 'industry_choices': industry_choices})

def skill_assessment_result(request, pk):
    assessment = get_object_or_404(models.SkillAssessment, pk=pk)
    context = {'assessment': assessment}
    return render(request, 'skill_assessment_result.html', context)

def skill_assessment_take(request, pk):
    assessment = get_object_or_404(models.SkillAssessment, pk=pk)
    context = {'assessment': assessment}
    return render(request, 'skill_assessment_take.html', context)

def skill_assessment_create(request):
    if request.method == "POST":
        # Handle form submission
        form = SkillAssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Skill assessment created successfully!")
        else:
            print(form.errors)
    else:
        form = SkillAssessmentForm()
    return render(request, 'skill_assessment_create.html', {'form': form})

def skill_assessment_list(request):
        assessments = SkillAssessment.objects.all()
        return render(request, 'skill_assessment/skill_assessment_list.html', {
        'assessments': assessments
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful upload
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})

def add_interview(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('interview_list')
        else:
            print(form.errors)
    else:
        form = InterviewForm()
    return render(request, 'add_interview.html', {'form': form})

def add_candidate(request):
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
        else:
            print(form.errors)
    else:
        form = CandidateProfileForm()
    return render(request, 'add_candidate.html', {'form': form})

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

@login_required
def interview_schedule(request):
    # Check if CV is uploaded
    application = models.Application.objects.filter(user=request.user).exists()
    if not application:
        return redirect('job_postings')

    if request.method == 'POST':
        # Save the interview schedule
        date = request.POST['date']
        time = request.POST['time']

        # Assuming InterviewScheduleForm is a ModelForm, create an instance
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            interview_schedule = form.save(commit=False)
            interview_schedule.user = request.user
            interview_schedule.save()

            # Send confirmation email
            send_mail(
                'Interview Scheduled',
                f'Your interview is scheduled on {date} at {time}.',
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )

            # Redirect to job postings page
            return redirect('job_postings')

    else:
        form = InterviewScheduleForm()

    return render(request, 'schedule_interview.html', {'form': form})

@login_required
def interview_complete(request):
    return render(request, 'interview_complete.html')

@csrf_protect
def my_protected_view(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            return redirect('success_url')
        else:
            print(form.errors)
    else:
        form = YourForm()
    return render(request, 'your_template.html', {'form': form})

def csrf_failure(request, reason=""):
    return render(request, '403_csrf.html', status=403)

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
def update_settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated successfully.')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error(s) below.')
            print(form.errors)
    else:
        form = SettingsForm(instance=request.user)
    return render(request, 'settings.html', {'form': form})
def home(request):
    return render(request, 'home.html')

def candidate_home(request):
    return render(request, 'candidate_home.html')

def employer_home(request):
    return render(request, 'employer_home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.profile = request.user.profile
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'job_create.html', {'form': form})

from django.shortcuts import get_object_or_404

def job_details(request, pk):
    job = get_object_or_404(Job, pk=pk)  # Returns 404 if not found
    return render(request, 'job_details.html', {'job': job})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(models.Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_details', pk=pk)
        else:
            print(form.errors)
    else:
        form = JobForm(instance=job)
    return render(request, 'job_edit.html', {'form': form})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(models.Job, pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user.profile
            application.save()
            return redirect('application_success')
        else:
            print(form.errors)
    else:
        form = JobApplicationForm()

    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'apply_job.html', context)

def job_list(request):
    # Get all jobs ordered by deadline (newest first)
    jobs = Job.objects.all()
    
    # Optional filters (example)
    company_name = request.GET.get('company_name')
    location = request.GET.get('location')
    
    if company_name:
        jobs = jobs.filter(company_name__icontains=company_name)
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    context = {
        'jobs': jobs,
        'search_company': company_name or '',
        'search_location': location or '',
    }
    return render(request, 'jobs/job_list.html', context)

def candidate_create(request):
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
        else:
            print(form.errors)
    else:
        form = InterviewForm()
    return render(request, 'interview_create.html', {'form': form})

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

class InterviewListView(ListView):
    model = models.Interview
    template_name = 'interview_list.html'
    context_object_name = 'interviews'
    paginate_by = 10  # Added pagination

class InterviewDetailView(DetailView):
    model = models.Interview
    template_name = 'interview_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Interview, pk=self.kwargs['pk'])  # Safe 404
    
@login_required
def interview_feedback(request, pk):
    interview = get_object_or_404(models.Interview, pk=pk)
    if request.method == 'POST':
        interview.feedback = request.POST['feedback']
        interview.save()
        return redirect('interview_detail', pk=pk)
    return render(request, 'interview_feedback.html', {'interview': interview})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
        else:
            print(form.errors)
    else:
        form = JobForm()
    return render(request, 'job_create.html', {'form': form})

@login_required
def candidate_list(request):
    candidates = models.Profile.objects.filter(is_candidate=True)
    return render(request, 'candidate_list.html', {'candidates': candidates})

@login_required
def interview_schedule(request):
    # Placeholder logic for scheduling interviews
    return render(request, 'interview_schedule.html')

@login_required
def interview(request):
    # Fetch the latest ongoing interview for the logged-in user
    interview = models.Interview.objects.filter(candidate=request.user, status='ongoing').first()
 # Redirect if no interview exists

    return render(request, 'interview.html', {'interview': interview})

    profile = Candidate.objects.get(user=interview.candidate)  # Fixed reference
    parsed_data = profile.cv_parsed_data

    # Retrieve all previous responses
    candidate_responses = models.CandidateResponse.objects.filter(interviews=interview).order_by('id')  # Fixed ivie

    if request.method == 'POST':
        current_question_id = request.POST.get('current_question_id')
        answer = request.POST.get('answer')

        if not current_question_id:
            return redirect('interview_page', interview_id=interview.id)

        try:
            question = models.Question.objects.get(id=current_question_id)
        except models.Question.DoesNotExist:
            return redirect('interview_page', interview_id=interview.id)

        # Save the candidate's response
        response = models.CandidateResponse.objects.create(
            interview=interview,
            question=question,
            answer=answer
        )

        # Generate follow-up question based on response
        follow_up_question = generate_next_question(answer)
        response.generated_follow_up = follow_up_question
        response.save()

        # Move to the next question
        interview.current_question_index += 1
        interview.save()

        return redirect('interview_page', interview_id=interview.id)

    # Fetch the next question
    generic_questions = models.Question.objects.filter(question_type='generic').order_by('order')[:3]

    if interview.current_question_index < 3:
        current_question = generic_questions[interview.current_question_index]
    else:
        cv_based_questions = generate_ai_questions(parsed_data)
        question_index_in_cv_section = interview.current_question_index - 3

        if question_index_in_cv_section < len(cv_based_questions):
            current_question = cv_based_questions[question_index_in_cv_section]
        else:
            last_response = candidate_responses.last()
            if last_response and last_response.generated_follow_up:
                current_question = last_response.generated_follow_up
            else:
                interview.status = 'completed'
                interview.save()
                return redirect('interview_complete')  # Fixed redirection

    return render(request, 'interview.html', {
        'current_question': current_question,
        'candidate_responses': candidate_responses
    })

@login_required
def job_application_list(request):
    applications = models.CVUpload.objects.filter(user=request.user)
    return render(request, 'job_application_list.html', {'applications': applications})

@login_required
def job_postings(request):
    if request.method == 'POST':
        form = Job(request.POST)
        if form.is_valid():
            form.save()  # ✅ Save job posting to the database
            return redirect('job_list')  # Redirect after saving
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = Job()

    return render(request, 'job_postings.html', {'form': form})

def update_settings(request):
    # Logic to update settings goes here
    return HttpResponse("Settings updated successfully!")

@login_required
def profile_update(request):
    return edit_profile(request)

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(CustomUserCreationForm, email=email)
        if user:
            # Handle password reset logic
            return redirect('home')
    return render(request, 'reset_password.html')

def contact(request):
    if request.method == 'POST':
        # Handle form submission
        return HttpResponse("Contact form submitted successfully!")

def get_interview_questions(request, interview_id):
    # Dummy placeholder — replace with DB logic later
    questions = [
        "What is your greatest achievement?",
        "Tell me about a difficult decision you had to make.",
        "How do you handle pressure?"
    ]
    return JsonResponse({'questions': questions})