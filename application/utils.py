import json
from myproject.settings import OPENAI_API_KEY
import openai
from some_speech_synthesis_library import synthesize_speech  # type: ignore
import speech_recognition as sr
import whisper
import spacy
from PyPDF2 import PdfReader

nlp = spacy.load('en_core_web_sm')

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

def conduct_interview(interview):
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

def generate_interview_question(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150,
    )
    return response.choices[0].text.strip()

def generate_questions(cv, candidate_answers):
    questions = []
    
    # Add 3 generic questions
    questions.extend([
        "Tell me about yourself.",
        "What are your strengths?",
        "Why do you want this job?"
    ])
    
    # Analyze the CV and add questions
    if cv:
        if 'Python' in cv.skills:
            questions.append("Describe your experience with Python.")
        if 'leadership' in cv.experience:
            questions.append("Tell us about a time you demonstrated leadership.")
    
    # Analyze candidate's previous answers for dynamic question generation
    for answer in candidate_answers:
        if "data analysis" in answer:
            questions.append("Can you explain your process for data analysis?")
        elif "teamwork" in answer:
            questions.append("How do you approach working in a team?")
    
    # Ensure the total number of questions doesn't exceed 10
    return questions[:10]

def generate_follow_up_question(answer):
    """Generate a follow-up question based on the candidate's response."""
    # Simple example: You can expand this to use an LLM like GPT to analyze the answer and suggest a follow-up
    if 'project' in answer.lower():
        return "Can you elaborate on the project you mentioned and the role you played?"
    elif 'team' in answer.lower():
        return "How did you collaborate with your team on this task?"
    else:
        return "Can you provide more details on this?"

def generate_questions_based_on_cv(cv_parsed_data):
    """Generate custom questions based on CV data."""
    questions = []
    skills = cv_parsed_data.get('skills', [])
    experience = cv_parsed_data.get('experience', [])

    for skill in skills:
        questions.append(f"How do you apply your {skill} skill in real-life scenarios?")
    
    for exp in experience:
        questions.append(f"Can you describe your experience working at {exp}?")
    
    return questions[:7]  # Limit to 7 questions based on CV
