
from datetime import datetime
from collections import defaultdict


class BehaviorTracker:

    def __init__(self):
        # user_id → list of interactions
        self.user_history = defaultdict(list)

    def log_interaction(self, user_id, text, score, level):
        entry = {
            "text": text,
            "score": score,
            "level": level,
            "time": datetime.now()
        }

        self.user_history[user_id].append(entry)

    def get_user_history(self, user_id):
        return self.user_history[user_id]

    def get_trend(self, user_id):
        history = self.get_user_history(user_id)

        if len(history) < 2:
            return "Stable"

        scores = [h["score"] for h in history]

        if scores[-1] > scores[0] + 20:
            return "Increasing"
        elif scores[-1] < scores[0] - 20:
            return "Decreasing"
        else:
            return "Stable"

    def detect_late_night(self, user_id):
        history = self.get_user_history(user_id)

        late_count = 0

        for h in history:
            hour = h["time"].hour
            if hour >= 23 or hour <= 4:
                late_count += 1

        return late_count >= 3

    def detect_repetition(self, user_id):
        history = self.get_user_history(user_id)

        texts = [h["text"] for h in history[-5:]]

        repeated_words = []

        for t in texts:
            words = t.lower().split()
            for w in words:
                if words.count(w) > 2:
                    repeated_words.append(w)

        return list(set(repeated_words))

    def detect_escalation(self, user_id):
        history = self.get_user_history(user_id)

        if len(history) < 3:
            return False

        last_levels = [h["level"] for h in history[-3:]]

        if last_levels == ["Low", "Medium", "High"]:
            return True

        if last_levels.count("High") >= 2:
            return True

        return False

    def get_behavior_summary(self, user_id):
        return {
            "trend": self.get_trend(user_id),
            "late_night": self.detect_late_night(user_id),
            "repetition": self.detect_repetition(user_id),
            "escalation": self.detect_escalation(user_id)
        }