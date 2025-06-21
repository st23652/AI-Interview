import os
import sys
import django
from django.conf import settings
from django.core.management import call_command
from django.urls import get_resolver, NoReverseMatch
from django.template.loader import get_template
from django.db import connection, ProgrammingError
from django.core.mail import send_mail, BadHeaderError

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def print_ok(msg): print(f"✅ {msg}")
def print_fail(msg): print(f"❌ {msg}")

def run_system_checks():
    print("\n🔍 Running Django system checks...")
    try:
        call_command('check', '--deploy', '--verbosity=1')
        print_ok("System checks passed")
    except Exception as e:
        print_fail(f"System checks failed: {e}")

def check_migrations():
    print("\n🔍 Checking for unapplied migrations...")
    from django.db.migrations.executor import MigrationExecutor
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    plan = executor.migration_plan(targets)
    if plan:
        print_fail("There are unapplied migrations:")
        for migration, _ in plan:
            print(f" - {migration.app_label}.{migration.name}")
    else:
        print_ok("No unapplied migrations")

def check_templates():
    print("\n🔍 Checking templates for loading and syntax errors...")
    # Get all template files under your templates directory
    templates_dir = os.path.join(settings.BASE_DIR, 'application', 'templates')
    error_found = False
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), templates_dir).replace('\\', '/')
                try:
                    # Load template, which also compiles and validates syntax
                    get_template(rel_path)
                except Exception as e:
                    print_fail(f"Template error in '{rel_path}': {e}")
                    error_found = True
    if not error_found:
        print_ok("All templates loaded without syntax errors")

def check_reverse_urls():
    print("\n🔍 Checking reverse URL resolution...")
    resolver = get_resolver()
    url_names = [name for name in resolver.reverse_dict.keys() if isinstance(name, str)]
    failed = False
    for name in sorted(url_names):
        try:
            # Reverse without arguments, so only url names without required args will succeed
            resolver.reverse_dict.getlist(name)
            from django.urls import reverse
            reverse(name)
            print_ok(f"Resolved URL '{name}'")
        except NoReverseMatch:
            print_fail(f"Cannot reverse URL: '{name}'")
            failed = True
        except Exception as e:
            print_fail(f"Error reversing URL '{name}': {e}")
            failed = True
    if not failed:
        print_ok("All named URLs reversed successfully")

def check_db_fields():
    print("\n🔍 Checking critical DB columns existence...")
    # Customize this list to your critical tables and fields to test presence
    checks = {
        'application_interview': ['id', 'candidate_id', 'job_id'],  # example from your error
        # Add more tables and columns if needed
    }
    with connection.cursor() as cursor:
        for table, columns in checks.items():
            for column in columns:
                try:
                    cursor.execute(f"SELECT {column} FROM {table} LIMIT 1;")
                except ProgrammingError as e:
                    print_fail(f"Missing column '{column}' in table '{table}': {e}")
                else:
                    print_ok(f"Found column '{column}' in table '{table}'")

"""def test_email_sending():
    print("\n🔍 Testing email backend (sending test email)...")
    try:
        send_mail(
            'Test Email from Diagnostic Check',
            'This is a test email to verify email backend settings.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # send to self
            fail_silently=False,
        )
        print_ok("Test email sent successfully")
    except BadHeaderError:
        print_fail("Bad header found in email")
    except Exception as e:
        print_fail(f"Failed to send test email: {e}")"""

def main():
    print("🔎 Starting Django Project Diagnostic Check")

    run_system_checks()
    check_migrations()
    check_templates()
    check_reverse_urls()
    check_db_fields()

    # Only test email if email backend and from email configured
    """if hasattr(settings, 'EMAIL_BACKEND') and settings.EMAIL_BACKEND != 'django.core.mail.backends.dummy.EmailBackend':
        if hasattr(settings, 'DEFAULT_FROM_EMAIL'):
            test_email_sending()
        else:
            print("⚠️ DEFAULT_FROM_EMAIL not set; skipping email test")
    else:
        print("⚠️ Email backend not configured or using dummy backend; skipping email test")"""

    print("\n✅ Diagnostic complete.")

if __name__ == '__main__':
    main()
