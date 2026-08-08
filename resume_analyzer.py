from pypdf import PdfReader


def extract_resume_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


if __name__ == "__main__":

    resume_text = extract_resume_text("resume.pdf")

    print("Resume Text:")
    print("----------------")
    print(resume_text)