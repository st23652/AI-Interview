import datetime
from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from .models import CustomUser, Interview, Job
from .views import send_interview_link

class EmailSendingTests(TestCase):

    def setUp(self):
        # Create a test job
        self.job = Job.objects.create(
            title='Software Engineer',
            company_name='Example Corp',
            description='Develop and maintain software solutions.',
            experience=3,
            job_type='Full-time',
            salary=70000,
            deadline=timezone.now() + timezone.timedelta(days=30)
        )

        # Create a test candidate
        self.candidate = CustomUser.objects.create_user(
            username='candidate1',
            email='candidate1@example.com',
            password='password'
        )

        # Create a test interviewer
        self.interviewer = CustomUser.objects.create_user(
            username='interviewer',
            email='interviewer@example.com',
            password='password'
        )

        # Create a test interview
        self.interview = Interview.objects.create(
            title='Technical Interview',
            description='Technical interview for the Software Engineer position.',
            candidate=self.candidate,
            interviewer=self.interviewer,
            scheduled_date=timezone.now() + timezone.timedelta(days=7),
            status='pending',  # Assuming 'pending' is a valid status
            question_set='problem_solving',
            answers={},
            feedback='',
            completed=False,
            job=self.job
        )

        # Set recruiter email for the test
        self.recruiter_email = 'recruiter@example.com'

    def test_send_interview_link(self):
        # Use the interview created in setUp
        interview = self.interview
        
        # Send the interview link email
        send_interview_link(interview.id, self.recruiter_email)

        # Check the latest sent email
        email = mail.outbox[0]
        
        # Dynamically create the expected interview link
        expected_link = f'/interviews/{interview.id}/'  # Adjust this path as needed

        # Validate the email content
        self.assertIn(expected_link, email.body)
        self.assertEqual(email.to, [self.recruiter_email])
        self.assertIn('Candidate Interview Link', email.subject)

    def test_email_link_functionality(self):
        # Test the auto-interview page rendering
        response = self.client.get('/auto-interview/')
        
        # Ensure the correct template is used
        self.assertTemplateUsed(response, 'auto_interview.html')

class EmailTemplateTests(TestCase):
    
    def test_email_template_rendering(self):
        # Dynamically create the expected interview link
        interview_link = reverse('get_next_question', args=[1])
        
        # Create context for the email template
        context = {
            'interview_link': interview_link,
            'recruiter_name': 'Recruiter',
        }
        
        # Render the email body using the template
        email_body = render_to_string('interview_link_email.html', context)
        
        # Check if the email body contains the link and proper content
        self.assertIn(interview_link, email_body)
        self.assertIn('Start Interview', email_body)
        self.assertIn('Recruiter', email_body)
