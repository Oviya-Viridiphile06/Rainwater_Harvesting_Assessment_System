from flask import Flask, request
from datetime import date

app = Flask(__name__)

# Rainfall Database (mm/year)

rainfall_data = {
    "Delhi": 790,
    "Mumbai": 2200,
    "Chennai": 1400,
    "Bangalore": 970,
    "Hyderabad": 800,
    "Kolkata": 1600,
    "Pune": 722,
    "Ahmedabad": 782,
    "Jaipur": 650,
    "Kochi": 3000,
    "Goa": 2900,
    "Shimla": 1500
}

# RCC Roof Standard

RUNOFF_COEFFICIENT = 0.8


# HOME PAGE

@app.route("/")
def home():
    options = "".join(
        f'<option value="{city}">{city}</option>'
        for city in rainfall_data
    )

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Rainwater Harvesting Assessment</title>
    <style>
        body {{
            margin:0;
            font-family:Segoe UI;
            background:url("/static/house.png") center/cover no-repeat fixed;
        }}
        .overlay {{
            background:rgba(0,0,0,0.65);
            min-height:100vh;
            padding-top:60px;
        }}
        .header {{
            text-align:center;
            color:white;
        }}
        .header h1 {{
            font-size:44px;
        }}
        .tagline {{
            font-size:20px;
            opacity:.9;
        }}
        .card {{
            background:white;
            width:420px;
            margin:40px auto;
            padding:30px;
            border-radius:14px;
            box-shadow:0 10px 30px rgba(0,0,0,.3);
        }}
        label {{
            font-weight:600;
        }}
        select,input {{
            width:100%;
            padding:12px;
            margin:8px 0 18px 0;
            border-radius:8px;
            border:1px solid #ccc;
        }}
        button {{
            width:100%;
            padding:14px;
            background:#2ecc71;
            border:none;
            color:white;
            font-size:17px;
            border-radius:8px;
            cursor:pointer;
        }}
        button:hover {{
            background:#27ae60;
        }}
        .footer {{
            text-align:center;
            color:white;
            opacity:.8;
            margin-top:20px;
        }}
    </style>
</head>
<body>
    <div class="overlay">
        <div class="header">
            <h1>🌧 Rainwater Harvesting Assessment</h1>
            <div class="tagline">
                Catch the Rain • Secure Tomorrow • Smart Water Sustainability System
            </div>
        </div>
        <div class="card">
            <form action="/calculate" method="get">
                <label>Location</label>
                <select name="location">{options}</select>
                <label>Catchment Area (m²)</label>
                <input type="number" step="0.1" name="area" required>
                <button type="submit">
                    Calculate Harvest Potential
                </button>
            </form>
        </div>
        <div class="footer">
            Urban Water Sustainability Assessment Portal
        </div>
    </div>
</body>
</html>
"""

# CALCULATION PAGE

@app.route("/calculate")
def calculate():
    location = request.args.get("location")
    area = request.args.get("area", type=float)

    if not location or area is None:
        return "<h3>Invalid Input</h3>"

    if area <= 0:
        return "<h3>Area must be greater than zero</h3>"

    rainfall = rainfall_data.get(location)

    if rainfall is None:
        return "<h3>Location not found</h3>"

    # ENGINEERING CALCULATION (CORRECT)

    harvested_water = (rainfall * area * RUNOFF_COEFFICIENT) / 1000
    daily_recharge = (harvested_water * 1000) / 365

    # Sustainability Rating
    
    if daily_recharge > 1500:
        rating = "Excellent Sustainability Potential"
        color = "#2ecc71"
    elif daily_recharge > 700:
        rating = "Moderate Sustainability"
        color = "#f39c12"
    else:
        rating = "Low Harvest Potential"
        color = "#e74c3c"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Harvesting Assessment Report</title>
    <style>
        body {{
            margin:0;
            background:#f4f7fb;
            font-family:Segoe UI;
        }}
        .header {{
            background:#0b3d91;
            color:white;
            padding:20px;
            text-align:center;
            font-size:24px;
            font-weight:bold;
        }}
        .report {{
            width:70%;
            margin:40px auto;
            background:white;
            padding:40px;
            border-radius:12px;
            box-shadow:0 6px 25px rgba(0,0,0,.1);
        }}
        .title {{
            text-align:center;
            font-size:34px;
            color:#1f4e79;
            margin-bottom:30px;
        }}
        .section {{
            margin-top:30px;
        }}
        .section h2 {{
            border-bottom:2px solid #eee;
            padding-bottom:8px;
            color:#2c3e50;
        }}
        .row {{
            display:flex;
            justify-content:space-between;
            padding:12px 0;
            border-bottom:1px solid #eee;
            font-size:18px;
        }}
        .value {{
            font-weight:bold;
            color:#1f7aec;
        }}
        .status {{
            margin-top:25px;
            padding:18px;
            border-radius:10px;
            text-align:center;
            font-size:20px;
            font-weight:bold;
            color:white;
            background:{color};
        }}
        .back {{
            display:block;
            text-align:center;
            margin-top:35px;
            font-weight:bold;
            text-decoration:none;
            color:#0b3d91;
        }}
    </style>
</head>
<body>
    <div class="header">
        Urban Rainwater Sustainability Assessment System
    </div>
    <div class="report">
        <div class="title">
            Substainability Report
        </div>
        <div style="text-align:right; color:#777;">
            Assessment Date: {date.today()}
        </div>
        <div class="section">
            <h2>🏠 Site Information</h2>
            <div class="row">
                <span>Location</span>
                <span class="value">{location}</span>
            </div>
            <div class="row">
                <span>Roof Catchment Area</span>
                <span class="value">{area} m²</span>
            </div>
            <div class="row">
                <span>Annual Rainfall</span>
                <span class="value">{rainfall} mm/year</span>
            </div>
            <div class="row">
                <span>Runoff Coefficient</span>
                <span class="value">{RUNOFF_COEFFICIENT}</span>
            </div>
        </div>
        <div class="section">
            <h2>💧 Harvesting Performance</h2>
            <div class="row">
                <span>Annual Harvested Water</span>
                <span class="value">{harvested_water:.2f} m³/year</span>
            </div>
            <div class="row">
                <span>Daily Recharge Potential</span>
                <span class="value">{daily_recharge:.2f} Litres/day</span>
            </div>
        </div>
        <div class="status">
            {rating}
        </div>
        <a class="back" href="/">← Perform New Assessment</a>
    </div>
</body>
</html>
"""

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
