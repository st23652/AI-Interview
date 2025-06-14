# application/test5_emotionDetection.py

from django.test import TestCase
from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from unittest.mock import patch
import sys


# OopCompanion:suppressRename

class EmotionDetectionTest(TestCase):

    def setUp(self):
        # Create a simple image for testing
        img = Image.new('RGB', (100, 100), color = 'red')
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        self.test_image = InMemoryUploadedFile(img_byte_arr, None, 'test_image.png', 'image/png', sys.getsizeof(img_byte_arr), None)

    @patch('application.views.detect_face_and_emotion')
    def test_process_image_emotion(self, mock_detect_face_and_emotion):
        # Mock the emotion detection function to return a predictable result
        mock_detect_face_and_emotion.return_value = {"emotion": "happy"}

        # Send a POST request to the `process_image` view with the test image
        response = self.client.post(reverse('process_image'), {'image': self.test_image})

        # Check if the response contains the expected emotion
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"emotion": "happy"})

    @patch('application.views.detect_face_and_emotion')
    def test_process_image_no_face(self, mock_detect_face_and_emotion):
        # Mock the emotion detection function to return an error (no face detected)
        mock_detect_face_and_emotion.return_value = {"error": "No face detected"}

        # Send a POST request to the `process_image` view with the test image
        response = self.client.post(reverse('process_image'), {'image': self.test_image})

        # Check if the response contains the expected error
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"error": "No face detected"})
