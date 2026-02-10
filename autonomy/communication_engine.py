
# autonomy/communication_engine.py

import logging
from typing import Optional
from api.database import SessionLocal
from api.models import UserCommunicationStyle

logger = logging.getLogger(__name__)

def get_user_style(user_id: str) -> UserCommunicationStyle:
    """Fetches user communication style or defaults."""
    db = SessionLocal()
    try:
        style = db.query(UserCommunicationStyle).filter(UserCommunicationStyle.user_id == user_id).first()
        if not style:
            style = UserCommunicationStyle(user_id=user_id)
            db.add(style)
            db.commit()
            db.refresh(style)
        return style
    finally:
        db.close()

def apply_communication_style(text: str, user_id: str = "default_user") -> str:
    """
    Modulates text based on user's style preferences.
    """
    style = get_user_style(user_id)
    
    # 1. Assertiveness Check (High Assertiveness -> Remove fluff)
    if style.assertiveness > 0.7:
        text = text.replace("I think ", "")
        text = text.replace("Maybe we should ", "Action required: ")
        text = text.replace("maybe we should ", "Action required: ") # handle lowercase
        text = text.replace("It seems like ", "")
        
    # 2. Verbosity Check (Short -> Summarize)
    # In a real system, we might use an LLM call here: "Summarize this: {text}"
    # For now, simplistic truncation or rule-based.
    if style.verbosity == "short":
        # Pseudo-summary: Split lines, take first few?
        # Or just prepend a marker for the UI to curb it.
        # Let's say we just forcefully tone it down.
        pass # Placeholder for advanced NLP

    # 3. Empathy Check (High Empathy -> Add softening)
    if style.empathy > 0.8:
        if "Failed" in text or "Error" in text:
            text = "I understand this is frustrating. " + text
            
    # 4. Tone (Simple keyword mods)
    if style.tone == "blunt":
        # Remove polite headers
        text = text.replace("Please note that", "Note:")
        text = text.replace("I recommend that you", "Do this:")
    elif style.tone == "motivational":
        if "Success" in text:
            text += " 🚀 Great momentum!"
            
    return text
