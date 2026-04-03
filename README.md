# 🚦 Nagpur Accident Intelligence Dashboard

A state-of-the-art predictive analytics dashboard designed to visualize and mitigate road accident hotspots in Nagpur. This project leverages clustering algorithms to identify high-risk zones and provides AI-tailored safety recommendations for urban road safety.

## 💎 Premium Features

- **Dynamic Hotspot Mapping**: Interactive spatial visualization of accident clusters using Folium and DBSCAN.
- **Modern Glassmorphism UI**: High-end dashboard interface with a sleek dark mode theme and Jakarta Sans typography.
- **Real-Time Analytics**: Instant calculation of Risk Index and safety prioritization.
- **Actionable Insights**: Automated localized safety strategies (speed breakers, improved lighting, police presence) for every identified hotspot.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- Pandas
- Folium

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/abhishekruikar7-rgb/nagpur-accident-hotspot-dashboard.git
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`.

## 🛠️ Technology Stack
- **Backend**: Python, Flask
- **Data Engineering**: Pandas, Scikit-learn (DBSCAN)
- **Visualization**: Folium (Leaflet.js)
- **Frontend**: HTML5, CSS3 (Glassmorphism, Dark Theme)

## 📊 Methodology
The system identifies hotspots by analyzing accident geospatial data (`latitude`, `longitude`) using Density-Based Spatial Clustering (DBSCAN). Clusters are then processed to determine the hotspot center and risk level, which the dashboard visualizes in real-time.

---
Developed with ❤️ for Nagpur Road Safety.
