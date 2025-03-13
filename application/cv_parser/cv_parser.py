import os
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import docx2txt
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_text_from_file(file_path):
    """Extract text from PDF or DOCX files."""
    if file_path.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
    elif file_path.endswith(".docx"):
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {e}")
    else:
        raise ValueError("Unsupported file format")

def calculate_similarity(cv_text, jd_text):
    """Calculate text similarity using TF-IDF and cosine similarity."""
    documents = [cv_text, jd_text]
    try:
        vectorizer = TfidfVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()
        similarity = cosine_similarity([vectors[0]], [vectors[1]])
        return similarity[0][0] * 100
    except Exception as e:
        raise ValueError(f"Error calculating similarity: {e}")

@csrf_exempt
def upload_files(request):
    """Handle CV and JD file uploads and return similarity score."""
    if request.method == "POST":
        cv_file = request.FILES.get("cv")
        jd_file = request.FILES.get("jd")

        if not cv_file or not jd_file:
            return JsonResponse({"error": "Both CV and Job Description files are required"}, status=400)

        cv_path = os.path.join(UPLOAD_FOLDER, cv_file.name)
        jd_path = os.path.join(UPLOAD_FOLDER, jd_file.name)

        # Save files properly
        cv_path_saved = default_storage.save(cv_path, ContentFile(cv_file.read()))
        jd_path_saved = default_storage.save(jd_path, ContentFile(jd_file.read()))

        # Get full absolute paths for debugging
        cv_full_path = default_storage.path(cv_path_saved)
        jd_full_path = default_storage.path(jd_path_saved)

        print(f"CV saved at: {cv_full_path}")
        print(f"JD saved at: {jd_full_path}")

        # Ensure files exist
        if not os.path.exists(cv_full_path):
            return JsonResponse({"error": f"CV file was not saved properly: {cv_full_path}"}, status=500)
        if not os.path.exists(jd_full_path):
            return JsonResponse({"error": f"JD file was not saved properly: {jd_full_path}"}, status=500)

        try:
            cv_text = extract_text_from_file(cv_full_path)
            jd_text = extract_text_from_file(jd_full_path)
            similarity_score = calculate_similarity(cv_text, jd_text)
            return JsonResponse({"similarity": f"{similarity_score:.2f}%"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "upload.html")
