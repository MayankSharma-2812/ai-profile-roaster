import pdfplumber

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
