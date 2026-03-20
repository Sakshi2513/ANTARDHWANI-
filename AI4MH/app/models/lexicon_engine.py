

class CrisisLexicon:

    def __init__(self):
        self.lexicon = {
            "critical": [
                "want to die",
                "end my life",
                "kill myself",
                "suicide",
                "no reason to live",
                "hopeless",
                "worthless",
                "i cant go on",
                "give up",
                "overdose",
                "cutting",
                "self harm"
            ],
            "stress": [
                "anxious",
                "tired",
                "overwhelmed",
                "lost",
                "afraid",
                "scared",
                "depressed",
                "insomnia",
                "crying",
                "alone"
            ]
        }

    def analyze(self, text):
        score = 0
        detected = []

        for category, words in self.lexicon.items():
            for word in words:
                if word in text:
                    detected.append(word)

                    if category == "critical":
                        score += 25
                    else:
                        score += 8

        return score, detected