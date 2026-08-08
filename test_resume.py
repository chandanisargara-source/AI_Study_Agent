from resume_analyzer import extract_text_from_pdf

pdf_path = "resume.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)