import os
import django
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
import unittest

# Set the settings module only if it's not already set
if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # Replace with your actual project name
    django.setup()


# OopCompanion:suppressRename

class DatabaseConnectionTest(unittest.TestCase):
    def test_database_connection(self):
        """Test if the database connection is successful."""
        db_conn = connections["default"]
        try:
            db_conn.cursor()
            self.assertTrue(True)  # Connection successful
        except OperationalError:
            self.fail("Database connection failed")

if __name__ == "__main__":
    unittest.main()
