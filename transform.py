import fitz

def extract_text_from_fitz(pdf_path):
    text=""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()

        return text
    except Exception as e:
        print(f"Error extracting text with PyMuPDF: {e}")
        return None
    
pdf_file = "DSP - Lecture Notes (Chapter 1).pdf"
extracted_string = extract_text_from_fitz(pdf_file)

if extracted_string:
    print(extracted_string)
    