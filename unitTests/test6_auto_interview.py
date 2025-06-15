# application/tests.py

from django.test import TestCase
from django.urls import reverse

class AutoInterviewPageTests(TestCase):
    def test_auto_interview_page_loads(self):
        url = reverse('auto_interview')  # Make sure this matches your URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auto_interview.html')

    def test_auto_interview_contains_video_and_buttons(self):
        response = self.client.get('/auto_interview/')  # or your URL pattern
        content = response.content.decode()

        self.assertIn('id="webcam"', content)  # Updated here
        self.assertIn('id="start-interview-btn"', content)
        self.assertIn('id="next-question-btn"', content)
        self.assertIn('id="start-record-btn"', content)
        self.assertIn('id="stop-record-btn"', content)

    
    

    
