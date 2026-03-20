import random
from collections import defaultdict


class GeoService:

    def __init__(self):
        self.region_data = defaultdict(list)

        self.locations = [
            ("Delhi", 28.6139, 77.2090),
            ("Mumbai", 19.0760, 72.8777),
            ("Bhopal", 23.2599, 77.4126),
            ("Indore", 22.7196, 75.8577),
            ("Bangalore", 12.9716, 77.5946),
            ("Hyderabad", 17.3850, 78.4867),
            ("Pune", 18.5204, 73.8567)
        ]

    def assign_location(self):
        return random.choice(self.locations)

    def log_region(self, city, score):
        self.region_data[city].append(score)

    def get_heatmap_data(self):
        heatmap = []

        for city, lat, lon in self.locations:
            scores = self.region_data.get(city, [0])
            avg_score = sum(scores) / len(scores)

            heatmap.append({
                "city": city,
                "lat": lat,
                "lon": lon,
                "intensity": avg_score
            })

        return heatmap

    def detect_alerts(self):
        alerts = []

        for city, scores in self.region_data.items():
            if len(scores) < 5:
                continue

            recent = scores[-5:]
            avg = sum(recent) / len(recent)

            if avg > 70:
                alerts.append(f"High crisis level in {city}")

        return alerts