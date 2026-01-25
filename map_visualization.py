import pandas as pd
import folium
import os

# Load hotspot data
base_dir = os.path.dirname(os.path.abspath(__file__))
hotspot_path = os.path.join(base_dir, "hotspots.csv")

df = pd.read_csv(hotspot_path)

# Normalize column names (safe)
df.columns = df.columns.str.strip().str.lower()

# Create Nagpur map
nagpur_map = folium.Map(
    location=[21.1458, 79.0882],
    zoom_start=12
)

# Plot hotspots
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=7,
        color="red",
        fill=True,
        fill_opacity=0.8
    ).add_to(nagpur_map)


# Save map
map_path = os.path.join(base_dir, "nagpur_hotspots.html")
nagpur_map.save(map_path)

print("Map created successfully")
print("Map saved at:", map_path)
