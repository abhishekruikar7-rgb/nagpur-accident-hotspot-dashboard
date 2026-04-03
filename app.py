from flask import Flask, render_template_string, jsonify
from engine import RealTimeEngine
import pandas as pd
import folium
import os

app = Flask(__name__)

# Initialize the Real-Time Accident Simulation Engine
engine = RealTimeEngine()
engine.start()

def get_live_map():
    state = engine.get_state()
    nagpur_lat, nagpur_lon = 21.1458, 79.0882
    
    # Initialize Map (Dark theme applied via CSS in template)
    m = folium.Map(location=[nagpur_lat, nagpur_lon], zoom_start=12, control_scale=True)
    
    hotspots = pd.DataFrame(state["hotspots"])
    if not hotspots.empty:
        centers = hotspots.groupby("cluster")[["latitude", "longitude"]].mean().reset_index()
        for _, row in centers.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"Live Hotspot-{int(row['cluster'])}",
                icon=folium.Icon(color="red", icon="warning", prefix="fa")
            ).add_to(m)
            
    # Add most recent activity as micro-dots
    for pt in state["recent_points"][-30:]:
        folium.CircleMarker(
            location=[pt["latitude"], pt["longitude"]],
            radius=3,
            color="#ff4757",
            fill=True,
            fill_opacity=0.6,
            weight=1
        ).add_to(m)
        
    return m._repr_html_()

@app.route("/api/data")
def api_data():
    state = engine.get_state()
    total = state["total_count"]
    hotspots_data = pd.DataFrame(state["hotspots"])
    total_hotspots = hotspots_data["cluster"].nunique() if not hotspots_data.empty else 0
    
    # Calculate Dynamic Risk Index
    risk_index = (total_hotspots * 1.5) if total > 0 else 0
    
    recommendation_text = [
        "Install speed breakers at accident-prone locations",
        "Increase traffic police presence during peak hours",
        "Improve street lighting in low visibility zones",
        "Install CCTV cameras for monitoring",
        "Place warning signboards near junctions",
        "Conduct road safety awareness campaigns",
        "Repair damaged roads and potholes"
    ]
    
    recs = pd.DataFrame({
        "Hotspot ID": [f"Hotspot-{i+1}" for i in range(min(total_hotspots, 7))],
        "Safety Recommendation": recommendation_text[:min(total_hotspots, 7)]
    })

    return jsonify({
        "total_accidents": total,
        "total_hotspots": total_hotspots,
        "risk_index": f"{risk_index:.1f}",
        "map_html": get_live_map(),
        "rec_table": recs.to_html(index=False, classes='table')
    })

@app.route("/")
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LIVE | Nagpur Accident Intelligence</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #ff4757;
            --success: #2ed573;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text: #f1f2f6;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: var(--text);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }

        .container { max-width: 1300px; margin: 0 auto; }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .live-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            color: var(--success);
            font-weight: 700;
            text-transform: uppercase;
        }

        .pulse {
            width: 10px;
            height: 10px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 0 rgba(46, 213, 115, 0.4);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(46, 213, 115, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(46, 213, 115, 0); }
            100% { box-shadow: 0 0 0 0 rgba(46, 213, 115, 0); }
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .card-label { color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px; }
        .card-value { font-size: 2.2rem; font-weight: 700; }

        .main-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }

        .map-section, .rec-section {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .map-container {
            height: 500px;
            border-radius: 16px;
            overflow: hidden;
            background: #111;
        }

        table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
        td { padding: 15px; background: rgba(255,255,255,0.03); font-size: 0.9rem; }
        tr td:first-child { border-radius: 12px 0 0 12px; color: var(--primary); font-weight: 700; }
        tr td:last-child { border-radius: 0 12px 12px 0; }

        /* Dark Mode Map Fix */
        .folium-map { filter: invert(0.9) hue-rotate(180deg) brightness(0.7); }

        @media (max-width: 1000px) {
            .main-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <div>
            <h1 style="margin:0; font-size: 1.8rem;">Nagpur Accident Intelligence</h1>
            <p style="margin:5px 0 0 0; color: #64748b;">Simulating Real-Time Incident Data Clustering</p>
        </div>
        <div class="live-indicator">
            <div class="pulse"></div> LIVE FEED ACTIVE
        </div>
    </div>

    <div class="stats-grid">
        <div class="card">
            <div class="card-label">Total Simulated Incidents</div>
            <div class="card-value" id="val-accidents">...</div>
        </div>
        <div class="card">
            <div class="card-label">Identified Hotspots</div>
            <div class="card-value" id="val-hotspots">...</div>
        </div>
        <div class="card">
            <div class="card-label">Current Risk Index</div>
            <div class="card-value" id="val-risk" style="color: var(--primary);">...</div>
        </div>
    </div>

    <div class="main-grid">
        <div class="map-section">
            <h3 style="margin-top:0">🗺️ Real-Time Spatial Analysis</h3>
            <div id="map-container" class="map-container">
                <!-- Map injected here -->
                <p style="text-align:center; padding-top:200px; color:#64748b;">Initializing LIVE Map View...</p>
            </div>
        </div>
        
        <div class="rec-section">
            <h3 style="margin-top:0">🚨 Active Safety Directives</h3>
            <div id="rec-container">
                <!-- Recs injected here -->
            </div>
        </div>
    </div>
</div>

<script>
    async function updateDashboard() {
        try {
            const res = await fetch('/api/data');
            const data = await res.json();
            
            document.getElementById('val-accidents').innerText = data.total_accidents;
            document.getElementById('val-hotspots').innerText = data.total_hotspots;
            document.getElementById('val-risk').innerText = data.risk_index;
            document.getElementById('rec-container').innerHTML = data.rec_table;
            
            // Map injection - simple innerHTML replacement
            // Note: Replacing the entire iframe might cause a slight blink
            const mapContainer = document.getElementById('map-container');
            mapContainer.innerHTML = data.map_html;
            
        } catch (e) {
            console.error("Dashboard update failed:", e);
        }
    }

    // Initial update
    updateDashboard();
    
    // Poll every 5 seconds
    setInterval(updateDashboard, 5000);
</script>

</body>
</html>
    """)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=False)

