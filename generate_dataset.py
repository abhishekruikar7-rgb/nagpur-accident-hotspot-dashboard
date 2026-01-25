import pandas as pd
import random

data = []

# FAR-APART Nagpur zones (no overlap)
nagpur_hotspot_zones = [
    (21.1497, 79.0828),  # Sitabuldi
    (21.1326, 79.0620),  # Dharampeth
    (21.0917, 79.0821),  # Manish Nagar
    (21.1702, 79.0823),  # Sadar
    (21.0895, 79.0476),  # Wardha Road
    (21.1815, 79.0550),  # Nandanvan
    (21.1402, 79.0950)   # Medical Square
]

for i, (base_lat, base_lon) in enumerate(nagpur_hotspot_zones):
    for _ in range(30):   # accidents per hotspot
        lat = base_lat + random.uniform(-0.0007, 0.0007)
        lon = base_lon + random.uniform(-0.0007, 0.0007)

        data.append({
            "latitude": lat,
            "longitude": lon
        })

df = pd.DataFrame(data)
df.to_csv("nagpur_accidents.csv", index=False)

print("Dataset created:", len(df), "records")
