from flask import Flask, render_template_string
import pandas as pd
import folium
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # -------- LOAD DATA --------
    accidents_path = os.path.join(base_dir, "nagpur_accidents.csv")
    hotspots_path = os.path.join(base_dir, "hotspots.csv")

    accidents = pd.read_csv(accidents_path)
    hotspots = pd.read_csv(hotspots_path)

    # -------- STATS --------
    total_accidents = len(accidents)

    if "cluster" in hotspots.columns:
        total_hotspots = hotspots["cluster"].nunique()
    else:
        total_hotspots = 0

    high_severity = total_accidents // 3  # estimated

    # -------- MAP --------
    nagpur_lat, nagpur_lon = 21.1458, 79.0882
    m = folium.Map(location=[nagpur_lat, nagpur_lon], zoom_start=12)

    if total_hotspots > 0:
        hotspot_centers = (
            hotspots
            .groupby("cluster")[["latitude", "longitude"]]
            .mean()
            .reset_index()
        )

        for _, row in hotspot_centers.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"Hotspot-{int(row['cluster'])}",
                icon=folium.Icon(color="red", icon="warning")
            ).add_to(m)
    else:
        folium.Marker(
            location=[nagpur_lat, nagpur_lon],
            popup="No hotspots detected",
            icon=folium.Icon(color="blue")
        ).add_to(m)

    map_html = m._repr_html_()

    # -------- SAFETY RECOMMENDATIONS --------
    recommendation_text = [
        "Install speed breakers at accident-prone locations",
        "Increase traffic police presence during peak hours",
        "Improve street lighting in low visibility zones",
        "Install CCTV cameras for monitoring",
        "Place warning signboards near junctions",
        "Conduct road safety awareness campaigns",
        "Repair damaged roads and potholes"
    ]

    recommendations = pd.DataFrame({
        "Hotspot ID": [f"Hotspot-{i+1}" for i in range(min(total_hotspots, 7))],
        "Safety Recommendation": recommendation_text[:min(total_hotspots, 7)]
    })

    # -------- HTML --------
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Nagpur Accident Intelligence Dashboard</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f6f9;
            padding: 20px;
        }
        h1 { color: #b71c1c; }
        .card {
            display: inline-block;
            background: white;
            padding: 15px;
            margin: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        th {
            background: #b71c1c;
            color: white;
            padding: 10px;
        }
        td {
            padding: 8px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>
<body>

<h1>🚦 Nagpur Accident Intelligence Dashboard</h1>

<div class="card">Total Accidents<br><b>{{ total_accidents }}</b></div>
<div class="card">Hotspots Identified<br><b>{{ total_hotspots }}</b></div>
<div class="card">High Severity (Estimated)<br><b>{{ high_severity }}</b></div>

<h2>🗺️ Accident Hotspot Map</h2>
{{ map_html | safe }}

<h2>🚨 Safety Recommendations</h2>
{{ rec_table | safe }}

</body>
</html>
""",
        total_accidents=total_accidents,
        total_hotspots=total_hotspots,
        high_severity=high_severity,
        map_html=map_html,
        rec_table=recommendations.to_html(index=False)
    )

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, use_reloader=False)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=False
    )
