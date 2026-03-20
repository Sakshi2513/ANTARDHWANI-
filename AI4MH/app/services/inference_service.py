# app/services/inference_service.py

from models.model import CrisisModel
from models.lexicon_engine import CrisisLexicon
from models.crisis_engine import compute_score
from services.behavior_service import BehaviorTracker
# GeoService is optional; if not implemented yet, we just simulate location
# from services.geo_service import GeoService

model = CrisisModel()
model.train()  # make sure your CSV path is correct

lexicon = CrisisLexicon()
tracker = BehaviorTracker()
# geo = GeoService()  # Optional for now


def analyze(text, user_id="user_1"):
    """
    Analyze user text and return structured result.
    """

    # Model prediction
    result = model.predict(text)

    # Lexicon scoring
    lex_score, words = lexicon.analyze(result.get("clean_text", text))

    # Crisis score computation
    score, level = compute_score(
        result.get("probabilities", [0.5, 0.5]),
        lex_score,
        result.get("label", "non-suicide")
    )

    # Log behavior
    tracker.log_interaction(user_id, text, score, level)

    behavior = tracker.get_behavior_summary(user_id)

    # Optional Geo data (simulated if GeoService not implemented)
    location = "Not available"  # fallback
    # Uncomment if GeoService is ready
    # location = geo.get_location(user_id, text)

    # Alerts (simulate)
    alerts = []
    if score > 75:  # High risk threshold
        alerts.append("High risk detected! Immediate attention required.")

    return {
        "label": result.get("label", "non-suicide"),
        "score": score,
        "level": level,
        "confidence": max(result.get("probabilities", [0, 0])),
        "keywords": words,
        "behavior": behavior,
        "location": location,
        "alerts": alerts
    }