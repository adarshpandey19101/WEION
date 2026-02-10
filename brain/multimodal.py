from tools.file_loader import load_file
from tools.audio import transcribe

def process_file(path: str) -> str:
    if path.endswith(".pdf") or path.endswith(".txt"):
        return load_file(path)

    if path.endswith(".mp3") or path.endswith(".wav"):
        return transcribe(path)

    return "Unsupported file type"
