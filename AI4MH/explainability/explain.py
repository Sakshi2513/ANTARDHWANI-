import numpy as np
from model import vectorizer, model

def explain_prediction(text):
    words = text.split()

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Transform input
    X = vectorizer.transform([text])
    coefficients = model.coef_[0]

    word_scores = {}

    for word in words:
        if word in feature_names:
            idx = list(feature_names).index(word)
            word_scores[word] = coefficients[idx]

    # Sort by importance
    sorted_words = sorted(word_scores.items(), key=lambda x: abs(x[1]), reverse=True)

    return sorted_words[:5]  # top 5 influential words