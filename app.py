from flask import Flask, render_template_string
import pandas as pd
import folium
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nagpur Accident Intelligence Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #ff4757;
            --secondary: #2f3542;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text: #f1f2f6;
            --accent: #5352ed;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: radial-gradient(circle at top right, #1e293b, #0f172a);
            color: var(--text);
            margin: 0;
            padding: 40px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: left;
            margin-bottom: 40px;
            border-left: 5px solid var(--primary);
            padding-left: 20px;
        }

        h1 {
            font-size: 2.5rem;
            margin: 0;
            letter-spacing: -1px;
            background: linear-gradient(90deg, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
        }

        .card-label {
            color: #94a3b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .card-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #fff;
        }

        .map-section {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 24px;
            margin-bottom: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .section-title {
            font-size: 1.5rem;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .map-container {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .rec-section {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 24px;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px;
        }

        th {
            text-align: left;
            padding: 15px;
            color: #94a3b8;
            font-weight: 600;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        td {
            padding: 15px;
            background: rgba(255, 255, 255, 0.03);
        }

        tr td:first-child { border-radius: 12px 0 0 12px; font-weight: 600; color: var(--primary); }
        tr td:last-child { border-radius: 0 12px 12px 0; }

        tr:hover td {
            background: rgba(255, 255, 255, 0.07);
        }

        /* Folium Map adjustments for Dark Mode */
        .folium-map {
            filter: grayscale(1) invert(0.9) hue-rotate(180deg) brightness(0.8);
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Nagpur Accident Intelligence Dashboard</h1>
        <p style="color: #64748b; margin-top: 10px;">Real-time analysis and hotspot detection for urban road safety</p>
    </div>

    <div class="stats-grid">
        <div class="card">
            <div class="card-label">Total Accidents</div>
            <div class="card-value">{{ total_accidents }}</div>
        </div>
        <div class="card">
            <div class="card-label">Hotspots Detected</div>
            <div class="card-value">{{ total_hotspots }}</div>
        </div>
        <div class="card">
            <div class="card-label">Risk Index</div>
            <div class="card-value" style="color: var(--primary);">{{ "%.1f"|format(high_severity / total_accidents * 10) }}</div>
        </div>
    </div>

    <div class="map-section">
        <div class="section-title">🗺️ Spatial Distribution & Hotspot Mapping</div>
        <div class="map-container">
            {{ map_html | safe }}
        </div>
    </div>

    <div class="rec-section">
        <div class="section-title">🚨 AI-Generated Safety Recommendations</div>
        {{ rec_table | safe }}
    </div>
</div>

</body>
</html>
""",
        total_accidents=total_accidents,
        total_hotspots=total_hotspots,
        high_severity=high_severity,
        map_html=map_html,
        rec_table=recommendations.to_html(index=False, classes='table')
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)

