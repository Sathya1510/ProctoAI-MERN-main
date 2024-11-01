# extract_text.py
import pdfplumber


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Check if the page has text
                text += page_text + "\n"  # Add a newline after each page
    return text
