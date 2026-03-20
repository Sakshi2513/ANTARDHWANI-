import random
import time

sample_messages = [
    "I feel so alone these days",
    "Nothing makes sense anymore",
    "I am just tired of everything",
    "Life is good today",
    "Feeling happy and motivated",
    "I don't want to wake up tomorrow",
    "Everything is falling apart",
    "I love my friends and family",
    "I can't handle this pain anymore",
    "Today was a productive day"
]


class SimulationService:

    def get_message(self):
        return random.choice(sample_messages)

    def stream(self, delay=2):
        while True:
            yield self.get_message()
            time.sleep(delay)

