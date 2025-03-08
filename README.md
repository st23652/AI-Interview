# AI Interviewer (In Progress)

## Overview
AI Interviewer is an advanced AI-powered platform designed to revolutionize the hiring process by automating job interviews. Using cutting-edge Natural Language Processing (NLP), speech recognition, and emotion detection technologies, the platform dynamically adapts interview questions based on candidate responses, providing a seamless and efficient experience for both candidates and recruiters.

## Key Features
- **Automated Question Generation**: The system intelligently formulates interview questions in real-time, tailoring them to the candidate’s responses and job requirements.
- **Speech Recognition & Analysis**: Utilizing OpenAI Whisper, the platform converts spoken answers into text for further processing and analysis.
- **Emotion Detection**: Integrates IBM Watson’s capabilities to assess the candidate’s emotions during the interview.
- **Fraud Prevention & Cheating Detection**: Future enhancements may include AI-powered vision analysis to detect dishonest behavior.
- **Candidate & Recruiter Dashboards**: Interactive dashboards for managing interview progress, reviewing responses, and assessing candidate performance.
- **Automated Email Notifications**: Candidates and recruiters receive timely email updates on interview scheduling, progress, and results.
- **Skill Assessment Integration**: Evaluates candidates based on predefined technical and behavioral competency benchmarks.
- **Data Security & Privacy**: Ensures compliance with industry standards for secure data handling and user privacy protection.

## Technology Stack
- **Frontend**: Angular (for an interactive and responsive user interface)
- **Backend**: Django with PostgreSQL (for robust and scalable backend operations)
- **AI Models**:
    - OpenAI GPT-4 (for NLP-driven question generation and response analysis)
    - OpenAI Whisper (for speech-to-text conversion)
    - IBM Watson (for emotion detection and analytics)
- **Deployment**: The platform will be hosted on a cloud infrastructure for optimal performance and accessibility.

## Development Progress
The project is currently under development and progressing through a structured five-phase lifecycle:

1. **Planning** - Completed
2. **Design** - Completed
3. **Development** - Ongoing
4. **Testing & Optimization** - Upcoming
5. **Deployment & Public Launch** - Future Phase

---

## Database Connection

To ensure that your PostgreSQL database is properly connected, follow these steps:

### 1. Check Connection via Command Line

#### **For Windows:**
1. Open PowerShell or Command Prompt.
2. Run:
```bash
   psql -U your_database_user -d your_database_name
```
   Replace your_database_user and your_database_name with actual values.
3. If prompted, enter the password.
4. Run a test query:
```bash
  SELECT 1;
```

#### **For Linux/macOS:**
1. Open Terminal.
2. Run:
```bash
  psql -U your_database_user -d your_database_name
```
3. Enter the password when prompted.
4. Run a test query:
```bash
  SELECT 1;
```

### 2. Check Connection in Django
1. Run the Django shell:
```bash
  python manage.py shell
```
2. Inside the shell, execute:
```bash
  from django.db import connections
  from django.db.utils import OperationalError

  db_conn = connections['default']
  try:
    db_conn.cursor()
    print("Database connection is successful!")
  except OperationalError as e:
    print(f"Database connection failed: {e}")
```

### 3. Verify PostgreSQL Service

#### **For Windows:**
1. Open Services (Win + R, then type services.msc).
2. Find PostgreSQL and ensure it is Running.

#### **For Linux/macOS:**
1. Run:
```bash
  sudo systemctl status postgresql
```
2. To start the service:
```bash
  sudo systemctl start postgresql
```

### 4. Check settings.py Configuration
Ensure your Django project has the correct database settings in settings.py:
```bash
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## Virtual Environment Setup
To manage dependencies efficiently, set up a virtual environment for your Django project.

### 1. Create a Virtual Environment
Navigate to your project directory and run:
```bash
  python -m venv venv
```
This will create a virtual environment named venv in your project directory.

### 2. Activate the Virtual Environment

#### **For Windows:**
```bash
  venv\Scripts\activate
```

#### **For Linux/macOS:**
```bash
  source venv/bin/activate
```
Once activated, your terminal prompt should change, indicating that the virtual environment is active.

### 3. Install Required Dependencies

With the virtual environment active, install the required packages:
```bash
  pip install -r requirements.txt
```
Ensure that requirements.txt contains all necessary dependencies for the project.

### 4. Deactivate the Virtual Environment

To deactivate the virtual environment, simply run:
```bash
  deactivate
```

### 5. Remove the Virtual Environment

If you need to remove the virtual environment, delete the venv folder:
```bash
  rm -rf venv  # For Linux/macOS
  rmdir /s /q venv  # For Windows
```

## Contribution & Feedback

Currently, contributions are not open as the core functionalities are being developed. However, constructive feedback and feature suggestions are encouraged to refine the platform further.

## Roadmap & Future Enhancements

1. **AI-Driven Vision Proctoring**: Implementing facial recognition and gaze-tracking for enhanced fraud detection.
2. **Expanded AI Capabilities**: Integration of additional AI models for deeper insights into candidate behavior.
3. **Multilingual Interview Support**: Supporting multiple languages to expand accessibility globally.
4. **Advanced Data Analytics & Reporting**: Detailed reports with insights into hiring trends, candidate performance, and interview efficiency.
5. **Mobile Compatibility**: Responsive design for mobile and tablet accessibility.
6. **Integration with HR Systems**: Enabling seamless data synchronization with existing Applicant Tracking Systems (ATS).

## Contact & Collaboration

For inquiries, feedback, or potential collaboration opportunities, please reach out to Sneha Tandon via [Linkedin](https://www.linkedin.com/in/sneha21042004/).

