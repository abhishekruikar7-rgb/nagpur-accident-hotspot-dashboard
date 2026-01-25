import pandas as pd
from sklearn.cluster import DBSCAN
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "nagpur_accidents.csv"))

coords = df[['latitude', 'longitude']]

dbscan = DBSCAN(
    eps=0.0015,      # 👈 SMALLER = more hotspots
    min_samples=6    # 👈 forces real clusters
)

df['cluster'] = dbscan.fit_predict(coords)

# remove noise
df = df[df['cluster'] != -1]

# save clustered points
df.to_csv("hotspots.csv", index=False)

print("Hotspot detection completed")
print("Number of hotspots found:", df['cluster'].nunique())
