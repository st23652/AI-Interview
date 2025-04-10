import os
from unittest.mock import patch

import django
from django.test import TestCase
from application.utils import generate_questions


# OopCompanion:suppressRename

class OpenAIGenerationTest(TestCase):

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    django.setup()

    @patch('application.utils.openai.ChatCompletion.create')  # Mock OpenAI API call
    def test_generate_questions_with_openai(self, mock_openai_call):
        """Test that OpenAI is used to generate questions based on the selected theme."""

        # Mock response from OpenAI
        mock_openai_call.return_value = {
            'choices': [{'message': {'content': 'What is AI?'}}]
        }

        theme = "Artificial Intelligence"
        response = generate_questions(theme)

        # Verify OpenAI API was called
        mock_openai_call.assert_called_once()

        # Verify the generated question is from OpenAI
        self.assertIn("What is AI?", response)

        # Ensure the API call includes the expected prompt
        expected_prompt = f"Generate a question related to {theme}"
        self.assertIn(expected_prompt, mock_openai_call.call_args[1]['messages'][0]['content'])
