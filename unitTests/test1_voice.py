import unittest
from unittest.mock import patch, MagicMock
from myapp.voice_gpt.voice_recognition_gpt import transcribe_audio

class TestVoiceRecognition(unittest.TestCase):
    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.AudioFile')
    @patch('speech_recognition.Recognizer.record')
    def test_transcribe_audio_success(self, mock_record, mock_audio_file, mock_recognize_google):
        # Setup mock for successful transcription
        mock_audio_file.return_value = MagicMock()
        mock_record.return_value = "mock_audio_data"
        mock_recognize_google.return_value = "Transcribed text successfully"

        result = transcribe_audio("test_audio.wav")
        self.assertEqual(result, "Transcribed text successfully")

    @patch('speech_recognition.AudioFile')
    def test_transcribe_audio_file_not_found(self, mock_audio_file):
        # Mock an invalid audio file
        mock_audio_file.side_effect = FileNotFoundError
        with self.assertRaises(ValueError) as context:
            transcribe_audio("nonexistent_audio.wav")

        self.assertEqual(str(context.exception), "Error in voice recognition: ")

if __name__ == '__main__':
    unittest.main()
