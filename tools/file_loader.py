from pypdf2 import PdfReader

def load_file(path: str) -> str:
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() for page in reader.pages)

    with open(path, "r", errors="ignore") as f:
        return f.read()
