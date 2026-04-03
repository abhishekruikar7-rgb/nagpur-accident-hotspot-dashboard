import pandas as pd
import random
import time
import threading
from sklearn.cluster import DBSCAN
from collections import deque

class RealTimeEngine:
    def __init__(self):
        self.max_records = 500
        self.accidents = deque(maxlen=self.max_records)
        self.hotspots = pd.DataFrame()
        self.lock = threading.Lock()
        self.is_running = False
        
        # Predefined Nagpur zones for clustered simulation
        self.zones = [
            {"name": "Sitabuldi", "lat": 21.1497, "lon": 79.0828, "risk": 0.8},
            {"name": "Dharampeth", "lat": 21.1326, "lon": 79.0620, "risk": 0.4},
            {"name": "Manish Nagar", "lat": 21.0917, "lon": 79.0821, "risk": 0.6},
            {"name": "Sadar", "lat": 21.1702, "lon": 79.0823, "risk": 0.9},
            {"name": "Wardha Road", "lat": 21.0895, "lon": 79.0476, "risk": 0.7},
            {"name": "Nandanvan", "lat": 21.1815, "lon": 79.0550, "risk": 0.3},
            {"name": "Medical Square", "lat": 21.1402, "lon": 79.0950, "risk": 0.5}
        ]

    def _generate_point(self):
        # Pick a zone based on risk weighting to create clusters
        zone = random.choices(self.zones, weights=[z["risk"] for z in self.zones])[0]
        # Add random scatter around the zone center
        lat = zone["lat"] + random.uniform(-0.0015, 0.0015)
        lon = zone["lon"] + random.uniform(-0.0015, 0.0015)
        return {"latitude": lat, "longitude": lon, "timestamp": time.time()}

    def _update_clusters(self):
        if len(self.accidents) < 10:
            return

        df = pd.DataFrame(list(self.accidents))
        coords = df[['latitude', 'longitude']]
        
        # INCREASED eps (0.002) and DECREASED min_samples (3) for easier clustering
        db = DBSCAN(eps=0.002, min_samples=3).fit(coords)
        df['cluster'] = db.labels_
        
        self.hotspots = df[df['cluster'] != -1].copy()

    def _shift_patterns(self):
        for zone in self.zones:
            change = random.uniform(-0.1, 0.1)
            zone["risk"] = max(0.1, min(1.0, zone["risk"] + change))

    def _run_loop(self):
        # INCREASED pre-population (200) to ensure immediate hotspots
        for _ in range(200):
            self.accidents.append(self._generate_point())
        self._update_clusters()

        while self.is_running:
            # Generate new "live" accident event
            new_pt = self._generate_point()
            
            with self.lock:
                self.accidents.append(new_pt)
                # Recalculate clusters as data evolves
                self._update_clusters()
            
            # Periodically shift the risk zones
            if random.random() < 0.1:
                self._shift_patterns()
                
            # Dynamic interval between 3 and 7 seconds
            time.sleep(random.uniform(3, 7))

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()

    def get_state(self):
        with self.lock:
            return {
                "total_count": len(self.accidents),
                "hotspots": self.hotspots.to_dict('records') if not self.hotspots.empty else [],
                "recent_points": list(self.accidents)[-50:] # latest 50 for the map
            }
