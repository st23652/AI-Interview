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
        url = reverse('auto_interview')
        response = self.client.get(url)
        content = response.content.decode()

        self.assertIn('<video', content)
        self.assertIn('id="videoPreview"', content)

        self.assertIn('id="startBtn"', content)
        self.assertIn('id="stopBtn"', content)

        self.assertIn('id="question"', content)
