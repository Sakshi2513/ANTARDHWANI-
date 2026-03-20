import random
import pandas as pd
from datetime import datetime, timedelta


class AnalyticsService:

    def __init__(self):
        self.history = []

    def log(self, score, level):
        self.history.append({
            "time": datetime.now(),
            "score": score,
            "level": level
        })

    def generate_dummy_data(self):
        now = datetime.now()

        data = []
        for i in range(30):
            data.append({
                "time": now - timedelta(minutes=i * 5),
                "score": random.randint(10, 100),
                "level": random.choice(["Low", "Medium", "High"])
            })

        return pd.DataFrame(data)

    def get_trend(self):
        if len(self.history) < 5:
            return self.generate_dummy_data()
        return pd.DataFrame(self.history)

    def get_distribution(self):
        df = self.get_trend()
        return df["level"].value_counts()