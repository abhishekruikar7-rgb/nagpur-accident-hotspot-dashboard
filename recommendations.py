import pandas as pd
import os

# Load hotspot data
base_dir = os.path.dirname(os.path.abspath(__file__))
hotspot_path = os.path.join(base_dir, "hotspots.csv")

df = pd.read_csv(hotspot_path)

recommendations = []

for cluster_id in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster_id]
    
    peak_hour = cluster_data['hour'].mode()[0]
    high_severity_count = (cluster_data['severity'] == 3).sum()
    
    action = (
        f"Increase traffic police and speed checks between "
        f"{peak_hour}:00 - {peak_hour+2}:00. "
        f"Install warning signboards and improve street lighting."
    )
    
    recommendations.append({
        "Hotspot Cluster": cluster_id,
        "Peak Risk Hour": peak_hour,
        "High Severity Accidents": high_severity_count,
        "Recommended Action": action
    })

# Save recommendations
output_path = os.path.join(base_dir, "safety_recommendations.csv")
pd.DataFrame(recommendations).to_csv(output_path, index=False)

print("Safety recommendations generated")
print("Saved at:", output_path)
