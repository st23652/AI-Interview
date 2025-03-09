import docx2txt
import os
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, upload_folder):
    if not is_allowed_file(file.filename):
        raise ValueError("File type not allowed.")
    
    file_path = os.path.join(upload_folder, file.filename)
    # Simulate saving file for the test
    open(file_path, 'w').close()
    return file_path

# Load a CV (PDF/DOCX)
def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        # Use PyPDF2 to extract text from PDFs
        try:
            reader = PdfReader(file_path)
            return ' '.join([page.extract_text() for page in reader.pages if page.extract_text() is not None])
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {e}")
    elif file_path.endswith('.docx') or file_path.endswith('.doc'):
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            raise ValueError(f"Error reading DOCX/DOC file: {e}")
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX files are supported.")

# Calculate similarity between CV and Job Description
def calculate_similarity(cv_text, jd_text):
    documents = [cv_text, jd_text]
    try:
        vectorizer = TfidfVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        return similarity[0][0]
    except Exception as e:
        raise ValueError(f"Error calculating similarity: {e}")

def main():
    # File Paths
    cv_file_path = "path_to_cv.pdf"  # Replace with your CV file path (PDF or DOCX)
    jd_text = """
    Enter your job description text here...
    """  # Add Job Description (JD) text manually or read from a file

    # Extract Text
    try:
        cv_text = extract_text_from_file(cv_file_path)
        similarity_score = calculate_similarity(cv_text, jd_text)
        print(f"CV and Job Description Similarity: {similarity_score * 100:.2f}%")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
