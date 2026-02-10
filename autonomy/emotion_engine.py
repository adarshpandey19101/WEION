
# autonomy/emotion_engine.py

import logging
from api.database import SessionLocal
from api.models import EmotionalMemory

logger = logging.getLogger(__name__)

def detect_emotion(user_id: str, trigger_event: str, context: str = "") -> str:
    """
    Infers emotion from triggers.
    """
    emotion = "CALM"
    intensity = 0.5
    
    if trigger_event == "GOAL_KILLED":
        emotion = "FRUSTRATED"
        intensity = 0.8
    elif trigger_event == "GOAL_FAILED":
        emotion = "STRESSED"
        intensity = 0.7
    elif trigger_event == "GOAL_COMPLETED":
        emotion = "CONFIDENT"
        intensity = 0.9
    elif trigger_event == "USER_OVERRIDE":
        emotion = "DETERMINED" # or Annoyed? Let's say Determined.
        intensity = 0.6
        
    # Save to DB
    db = SessionLocal()
    try:
        mem = EmotionalMemory(
            user_id=user_id,
            emotion=emotion,
            trigger_event=trigger_event,
            intensity=intensity,
            context=context
        )
        db.add(mem)
        db.commit()
        # logger.info(f"❤️ Emotion Detected: {emotion} ({intensity})")
    finally:
        db.close()
        
    return emotion

def get_current_emotion(user_id: str) -> str:
    """Returns latest emotion."""
    db = SessionLocal()
    try:
        last = db.query(EmotionalMemory).filter(EmotionalMemory.user_id == user_id).order_by(EmotionalMemory.id.desc()).first()
        if last:
            return last.emotion
        return "CALM"
    finally:
        db.close()

def get_emotional_bias(emotion: str) -> float:
    """
    Returns a score modifier based on emotion.
    Stressed -> Penalize Risk.
    Confident -> Boost Risk?
    """
    if emotion == "STRESSED":
        return -0.1 # Be careful
    elif emotion == "FRUSTRATED":
        return -0.2 # Stop annoying user
    elif emotion == "CONFIDENT":
        return 0.1 # Go for it
    return 0.0
