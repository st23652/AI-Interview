import fitz  # PyMuPDF
import docx
from fuzzywuzzy import fuzz
from fpdf import FPDF
import os

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT files."""
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_path.endswith(".docx") or file_path.endswith(".doc"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise ValueError("Unsupported file format. Use PDF, TXT, DOC, or DOCX.")

def compare_texts(cv_text, job_text):
    """Compare the CV text and job description text based on key sections."""
    sections = ["Skills", "Experience", "Education", "Certifications", "Summary"]
    scores = {section: fuzz.token_set_ratio(cv_text.lower(), job_text.lower()) for section in sections}
    overall_score = sum(scores.values()) // len(scores)
    return scores, overall_score

def generate_pdf_report(cv_path, job_path, scores, details, overall_score):
    """Generate a detailed PDF report comparing CV and job description."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font to Arial (safe for encoding issues)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "CV vs Job Description Detailed Report", ln=True, align='C')

    # File Names
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"CV File: {cv_path}", ln=True)
    pdf.cell(200, 10, f"Job Description File: {job_path}", ln=True)
    pdf.ln(10)

    # Section-wise details
    for section, info in details.items():
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, f"{section} Match Score: {info['score']}%", ln=True)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, info["description"])

        pdf.ln(5)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, "Matching Elements:", ln=True)
        pdf.set_font("Arial", size=12)
        for match in info["matching"]:
            text = f"- {match}"  # Replace • with -
            pdf.cell(200, 10, text.encode('latin-1', 'replace').decode('latin-1'), ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, "Missing Elements:", ln=True)
        pdf.set_font("Arial", size=12)
        for missing in info["missing"]:
            text = f"- {missing}"  # Replace • with -
            pdf.cell(200, 10, text.encode('latin-1', 'replace').decode('latin-1'), ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, "Suggestions for Improvement:", ln=True)
        pdf.set_font("Arial", size=12)
        text = info["suggestions"]
        pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))

        pdf.ln(10)

    # Overall Score
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, f"Overall Match Score: {overall_score}%", ln=True, align='C')

    # Save the PDF
    output_path = "Detailed_Comparison_Report.pdf"
    pdf.output(output_path, "F")
    print(f"Report saved as {output_path}")

if __name__ == "__main__":
    # Define paths to CV and Job Description files
    cv_file = "C:/AI-Interview/application/cv_parser/uploads/Sneha_Infosys_CV.pdf"  # Change to actual file path
    job_file = "C:/AI-Interview/application/cv_parser/uploads/JDsample1.txt"  # Change to actual file path

    # Extract text from both files
    cv_text = extract_text(cv_file)
    job_text = extract_text(job_file)

    # Compare the extracted texts
    scores, overall_score = compare_texts(cv_text, job_text)

    # Detailed information for sections (this can be enhanced to match real data)
    details = {
        "Skills": {
            "score": scores["Skills"],
            "description": "The Skills section compares the required skills from the job description with the skills listed in the CV.",
            "matching": ["Python", "Machine Learning", "Data Analysis", "Django", "Flask"],  # Example matching skills
            "missing": ["Deep Learning", "Cloud Computing", "Data Engineering"],  # Example missing skills
            "suggestions": "Consider adding any additional programming languages or frameworks that are relevant to the role."
        },
        "Experience": {
            "score": scores["Experience"],
            "description": "The Experience section matches the job's required experiences with what is mentioned in the CV.",
            "matching": ["Software Developer", "Project Management", "Team Leadership"],  # Example matching experiences
            "missing": ["Data Scientist", "Full-stack Development"],  # Example missing experiences
            "suggestions": "Provide more details on the tools used and highlight any specific technologies like AI, Data Science, or Cloud."
        },
        "Education": {
            "score": scores["Education"],
            "description": "This section checks the educational background and compares it with the job's educational requirements.",
            "matching": ["BSc in Artificial Intelligence", "Computer Science Coursework"],  # Example matching education
            "missing": ["Masters in Computer Science", "PhD in AI"],  # Example missing education
            "suggestions": "Consider mentioning any coursework or relevant projects in AI/ML to strengthen this section."
        },
        "Certifications": {
            "score": scores["Certifications"],
            "description": "This section evaluates the certifications relevant to the job role.",
            "matching": ["Certified Python Developer", "AWS Certified Solutions Architect"],  # Example matching certifications
            "missing": ["Google Cloud Certified", "Azure Fundamentals"],  # Example missing certifications
            "suggestions": "Add certifications that are relevant to the job, especially cloud computing or specific technologies mentioned in the job description."
        },
        "Summary": {
            "score": scores["Summary"],
            "description": "The Summary section compares the general job fit and overall narrative of the CV to the job description.",
            "matching": ["Self-motivated", "Team-oriented", "Problem-solving skills"],  # Example matching summary keywords
            "missing": ["Leadership skills", "AI-focused career goals"],  # Example missing summary elements
            "suggestions": "Revise the summary to align more closely with the job's expectations, emphasizing leadership and technical expertise."
        }
    }

    # Generate the PDF report
    generate_pdf_report(cv_file, job_file, scores, details, overall_score)
