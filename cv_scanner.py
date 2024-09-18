import os
from pyresparser import ResumeParser
import nltk
from nltk.tokenize import word_tokenize
import spacy
from pyresparser import ResumeParser

# Load the spaCy model directly
nlp = spacy.load('en_core_web_sm')

# Ensure pyresparser uses the loaded model
data = ResumeParser(resume_path, nlp=nlp).get_extracted_data()

# Download stopwords if not already present
nltk.download('stopwords')

def extract_text_from_resume(resume_path):
    """
    Extract text from the resume PDF.
    """
    data = ResumeParser(resume_path).get_extracted_data()
    return data['text'] if 'text' in data else ''

def rank_candidates(resumes, job_description):
    """
    Rank candidates based on the job description and resume content.
    """
    job_tokens = set(word_tokenize(job_description.lower()))
    ranked_candidates = []

    for resume in resumes:
        resume_text = extract_text_from_resume(resume['file_path'])
        resume_tokens = set(word_tokenize(resume_text.lower()))
        matched_keywords = job_tokens.intersection(resume_tokens)
        score = len(matched_keywords)
        
        ranked_candidates.append({
            'candidate': resume['candidate'],
            'score': score,
            'matched_keywords': list(matched_keywords)
        })

    return sorted(ranked_candidates, key=lambda x: x['score'], reverse=True)

def main():
    """
    Main function to execute the CV scanning and ranking process.
    """
    # Load job description from file
    with open('job_description.txt', 'r') as file:
        job_description = file.read()

    # Example resumes
    resumes = [
        {'candidate': 'John Doe', 'file_path': 'resumes/john_doe_resume.pdf'},
        {'candidate': 'Jane Smith', 'file_path': 'resumes/jane_smith_resume.pdf'}
    ]

    ranked_candidates = rank_candidates(resumes, job_description)

    print("Ranked Candidates:")
    for candidate in ranked_candidates:
        print(f"Candidate: {candidate['candidate']}, Score: {candidate['score']}, Matched Keywords: {candidate['matched_keywords']}")

if __name__ == "__main__":
    main()
