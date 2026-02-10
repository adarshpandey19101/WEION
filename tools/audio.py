from faster_whisper import WhisperModel

model = WhisperModel("base")

def transcribe(path: str) -> str:
    segments, _ = model.transcribe(path)
    return " ".join(segment.text for segment in segments)
