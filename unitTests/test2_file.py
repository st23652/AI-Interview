import unittest
import os
from unittest.mock import MagicMock, patch
from myapp.cv_parser.cv_parser import is_allowed_file, save_file

class TestFileUploader(unittest.TestCase):
    def setUp(self):
        # Prepare a mock upload folder for testing
        self.upload_folder = "mock_upload_folder"
        os.makedirs(self.upload_folder, exist_ok=True)

    def tearDown(self):
        # Clean up created files after tests
        for file in os.listdir(self.upload_folder):
            os.remove(os.path.join(self.upload_folder, file))
        os.rmdir(self.upload_folder)

    def test_is_allowed_file(self):
        self.assertTrue(is_allowed_file("resume.pdf"))
        self.assertTrue(is_allowed_file("document.docx"))
        self.assertFalse(is_allowed_file("script.exe"))

    def test_save_file_valid(self):
        mock_file = MagicMock()
        mock_file.filename = "resume.pdf"

        result = save_file(mock_file, self.upload_folder)
        self.assertTrue(os.path.exists(result))

    def test_save_file_invalid(self):
        mock_file = MagicMock()
        mock_file.filename = "virus.exe"

        with self.assertRaises(ValueError) as context:
            save_file(mock_file, self.upload_folder)

        self.assertEqual(str(context.exception), "File type not allowed.")

if __name__ == '__main__':
    unittest.main()
