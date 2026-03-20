import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from pipelines.preprocessing import clean_text


class CrisisModel:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2)
        )
        self.model = LogisticRegression()
        self.is_trained = False

    def map_labels(self, label):
        if label == "suicide":
            return "Critical"
        else:
            return "Normal"

    def train(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.join(base_dir, "data", "data.csv")

        df = pd.read_csv(data_file)

        df["text"] = df["text"].apply(clean_text)
        df["label"] = df["class"].apply(self.map_labels)

        X = self.vectorizer.fit_transform(df["text"])
        y = df["label"]

        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, text):
        if not self.is_trained:
            raise Exception("Model not trained")

        text_clean = clean_text(text)
        X = self.vectorizer.transform([text_clean])

        prediction = self.model.predict(X)[0]
        probs = self.model.predict_proba(X)[0]

        return {
            "label": prediction,
            "probabilities": probs,
            "clean_text": text_clean
        }