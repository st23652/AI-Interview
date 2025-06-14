import json
import openai
import speech_recognition as sr
import whisper
import spacy
import pyttsx3  # Added for text-to-speech
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import numpy as np
import cv2
from deepface import DeepFace

def detect_face_and_emotion(image):
    # Convert uploaded image to OpenCV format
    img_array = np.fromstring(image.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If a face is detected, analyze emotion
    if len(faces) > 0:
        # Use DeepFace to detect emotion
        result = DeepFace.analyze(img, actions=['emotion'])
        return {"emotion": result[0]['dominant_emotion']}
    else:
        return {"error": "No face detected"}

# Load environment variables from the .env file
load_dotenv()

# Access the OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

nlp = spacy.load('en_core_web_sm')

# Initialize text-to-speech engine
engine = pyttsx3.init()

def evaluate_answer(job_role, question, candidate_answer):
    prompt = f"""
    You are an AI interviewer for a {job_role} position.
    The candidate was asked: "{question}"
    They responded: "{candidate_answer}"

    Provide detailed feedback on their response, including:
    1. Strengths
    2. Areas for improvement
    3. A final rating (out of 10)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert interviewer providing feedback."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

def synthesize_speech(text):
    """Convert text to speech using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def extract_text_from_cv(cv_file):
    """Extract text from PDF CV."""
    reader = PdfReader(cv_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_skills_and_experience(cv_text):
    """Parse skills and experience from CV text using NLP."""
    doc = nlp(cv_text)
    skills = []
    experience = []
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':  # Example: Capture organizations for experience
            experience.append(ent.text)
        elif ent.label_ == 'SKILL':  # Capture skills (define this entity in custom NLP if needed)
            skills.append(ent.text)
    
    return {
        'skills': skills,
        'experience': experience
    }

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result['text']

def recognize_speech(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def parse_resume(resume_file):
    parsed_data = {}
    # Placeholder code to parse resume
    return parsed_data

def parse_job_description(description):
    parsed_data = {}
    # Placeholder code to parse job description
    return parsed_data

def conduct_interview(interview, synthesize_speech=None):
    transcript = []
    questions = generate_questions(interview.job.parsed_description, interview.candidate.parsed_resume)
    for question in questions:
        synthesize_speech(question)
        response = recognize_speech()
        transcript.append({'question': question, 'response': response})
        deeper_questions = generate_deeper_questions(response)
        for dq in deeper_questions:
            synthesize_speech(dq)
            deeper_response = recognize_speech()
            transcript.append({'question': dq, 'response': deeper_response})
    interview.transcript = json.dumps(transcript)
    interview.emotional_state = assess_emotional_state()
    interview.cheating_detected = detect_cheating()
    interview.noise_reduction_applied = apply_noise_cancellation()
    interview.save()

def generate_questions(job_data, resume_data):
    questions = []
    # Placeholder code to generate questions
    return questions

def generate_deeper_questions(response):
    deeper_questions = []
    # Placeholder code to generate deeper questions
    return deeper_questions

def assess_emotional_state():
    emotions = {}
    # Placeholder code to assess emotional state using computer vision
    return emotions

def detect_cheating():
    cheating = False
    # Placeholder code to detect cheating using computer vision
    return cheating

def apply_noise_cancellation():
    noise_reduction = False
    # Placeholder code to apply noise cancellation
    return noise_reduction

def generate_interview_question(job_role, previous_answer):
    prompt = f"""
    You are an AI interviewer for a {job_role} position.
    The candidate just answered: "{previous_answer}".
    Based on this, generate the next relevant interview question.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional interviewer."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Example usage
if __name__ == "__main__":
    question = "Describe your experience working with Python."
    print("Question:", question)
    print("Speaking the question...")
    synthesize_speech(question)
