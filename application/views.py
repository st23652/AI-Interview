from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
import openai
from . import models
from .forms import CVForm, CandidateProfileForm, JobApplicationForm, JobForm, ProfileForm, SettingsForm, InterviewScheduleForm, CustomUserCreationForm, InterviewForm, SkillAssessmentForm, UserRegistrationForm, YourForm
from .forms import AnswerForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from .serializers import ProfileSerializer
from .forms import ProfilePictureForm
from django.views.decorators.csrf import csrf_exempt
from openai import ChatCompletion
from django.template.loader import render_to_string
import spacy
from pdfminer.high_level import extract_text
from .forms import ResumeUploadForm
from spacy.matcher import Matcher
from rest_framework import viewsets
from .serializers import InterviewSerializer, JobSerializer, CustomUserSerializer
from .forms import InterviewFeedbackForm
import os
from dotenv import load_dotenv

load_dotenv()

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
            response_text=data['response']
        )
        return JsonResponse({'status': 'success'})

def interview_feedback(request, interview_id):
    interview = get_object_or_404(models.Interview, id=interview_id)

    if request.method == 'POST':
        form = InterviewFeedbackForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('interview_detail', interview_id=interview.id)  # Redirect to the interview detail page or any other page
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
    return redirect('login')

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

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume_text = parse_resume_text(resume.file.path)
            resume.parsed_text = resume_text

            # Extract information
            extracted_info = extract_information(resume_text)
            resume.skills = extracted_info['skills']
            resume.experience = extracted_info['experience']
            resume.education = extracted_info['education']

            resume.save()
            return redirect('resume_success')

    else:
        form = ResumeUploadForm()
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

def send_interview_link(interview_id, recruiter_email):
    try:
        interview = models.Interview.objects.get(id=interview_id)
        interview_link = f"http://127.0.0.1:8000/interviews/{interview_id}/"
        
        subject = "Candidate Interview Link"
        message = render_to_string('interview_link_email.html', {
            'interview_link': interview_link,
            'recruiter_name': 'Recruiter',
        })
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recruiter_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")
        # Log error or notify administrator

@csrf_exempt
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

def generate_ai_questions(job_position):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Generate 5 interview questions for the position of {job_position}."
    response = ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return [message['content'] for message in response['choices'][0]['message']]

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

def profile_view(request):
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
        profile = request.user.profile
    except models.Profile.DoesNotExist:
        profile = models.Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)

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
    assessments = models.SkillAssessment.objects.all()
    return render(request, 'skill_assessment_list.html', {'assessments': assessments})

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

def interview(request):
    interviews = models.Interview.objects.all()
    return render(request, 'interview.html', {'interviews': interviews})

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
def interview_list(request):
    sectors = models.Sector.objects.all()
    return render(request, 'interview_list.html', {'sectors': sectors})

@login_required
def interview_detail(request, sector_id):
    sector = get_object_or_404(models.Sector, id=sector_id)
    questions = models.Question.objects.filter(sector=sector).order_by('order')
    if request.method == 'POST':
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer:
                models.CandidateResponse.objects.create(
                    candidate=request.user,
                    question=question,
                    answer=answer
                )
        return redirect('interview_complete')
    return render(request, 'interview_detail.html', {'sector': sector, 'questions': questions})

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

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registration successful.'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

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

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user using email
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or another page
            else:
                messages.error(request, "Invalid email or password.")
                return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def candidate_home(request):
    return render(request, 'candidate_home.html')

def employer_home(request):
    return render(request, 'employer_home.html')

@login_required
def profile(request):
    profile = get_object_or_404(models.Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

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

@login_required
def job_details(request, pk):
    job = get_object_or_404(models.Job, pk=pk)
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

@login_required
def job_list(request):
    jobs = models.Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

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

@login_required
def interview_detail(request, pk):
    interview = get_object_or_404(models.Interview, pk=pk)
    return render(request, 'interview_detail.html', {'interview': interview})

@login_required
def interview_feedback(request, pk):
    interview = get_object_or_404(models.Interview, pk=pk)
    if request.method == 'POST':
        interview.feedback = request.POST['feedback']
        interview.save()
        return redirect('interview_detail', pk=pk)
    return render(request, 'interview_feedback.html', {'interview': interview})

@login_required
def interview_list(request):
    interviews = models.Interview.objects.all()
    return render(request, 'interview_list.html', {'interviews': interviews})

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
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user.profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def interview_schedule(request):
    # Placeholder logic for scheduling interviews
    return render(request, 'interview_schedule.html')

@login_required
def interview(request, interview_id):
    interview = models.Interview.objects.get(id=interview_id)
    profile = CandidateProfile.objects.get(user=interview.candidate)
    parsed_data = profile.cv_parsed_data

    # Retrieve all previous responses
    candidate_responses = models.CandidateResponse.objects.filter(interview=interview).order_by('id')
    
    # Step 1: Handle POST request to capture response and generate follow-up questions
    if request.method == 'POST':
        current_question_id = request.POST.get('current_question_id')
        answer = request.POST.get('answer')

        # Save the candidate's response
        question = models.Question.objects.get(id=current_question_id)
        response = models.CandidateResponse.objects.create(
            interview=interview,
            question=question,
            answer=answer
        )

        # Generate follow-up question based on response
        follow_up_question = generate_follow_up_question(answer)
        response.generated_follow_up = follow_up_question
        response.save()

        # Move to the next question
        interview.current_question_index += 1
        interview.save()

        # Redirect to refresh page and show next question
        return redirect('interview_page', interview_id=interview.id)

    # Step 2: Fetch the next question to ask
    generic_questions = models.Question.objects.filter(question_type='generic').order_by('order')[:3]

    # Step 3: After the first 3 questions, generate CV-based questions
    if interview.current_question_index < 3:
        current_question = generic_questions[interview.current_question_index]
    else:
        cv_based_questions = generate_questions_based_on_cv(parsed_data)
        question_index_in_cv_section = interview.current_question_index - 3

        if question_index_in_cv_section < len(cv_based_questions):
            current_question = cv_based_questions[question_index_in_cv_section]
        else:
            # If we have processed all CV-based questions, ask follow-up questions
            last_response = candidate_responses.last()
            if last_response and last_response.generated_follow_up:
                current_question = last_response.generated_follow_up
            else:
                # Mark interview as complete
                interview.status = 'completed'
                interview.save()
                return redirect('interview.html')

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
    if request.method == 'GET':
        jobs = models.Job.objects.all()
        return render(request, 'job_postings.html', {'jobs': jobs})
    
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
