from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your chromedriver
service = Service("C:/Users/5688s/chromedriver-win64/chromedriver-win64/chromedriver.exe")  # <-- Replace with actual path
driver = webdriver.Chrome(service=service)

# Base URL with trailing slash
BASE_URL = 'http://localhost:8000/'

# Define paths with leading slash only
pages = {
    "Home": "home/",
    "Login": "login/",
    "Register": "register/",
    "Candidate Dashboard": "candidate/dashboard/",
    "Employer Dashboard": "employer/dashboard/",
    "Job List": "jobs/",
    "Interview Practice": "interview/practice/",
}

# Function to test page loading
def test_page(name, path):
    url = BASE_URL + path
    try:
        driver.get(url)
        time.sleep(1.5)
        print(f"✅ {name} loaded: {url}")
    except Exception as e:
        print(f"❌ {name} failed: {url}\nError: {e}")

# Run the tests
for name, path in pages.items():
    test_page(name, path)

driver.quit()
