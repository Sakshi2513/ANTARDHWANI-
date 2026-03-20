
def compute_score(probabilities, lexicon_score, label):

    # Base score
    if label == "Critical":
        base = 70
    else:
        base = 20

    final_score = min(100, base + lexicon_score)

    if final_score < 30:
        level = "Low"
    elif final_score < 70:
        level = "Medium"
    else:
        level = "High"

    return final_score, level