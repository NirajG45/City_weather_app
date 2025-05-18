from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "f82d429e6a4cb8fecadd760ca2c4a2ed"  # <-- अपनी API Key डालो

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    chart_data = []

    if request.method == "POST":
        city = request.form.get("city")
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"

        geo_res = requests.get(geo_url).json()
        if geo_res:
            lat = geo_res[0]["lat"]
            lon = geo_res[0]["lon"]

            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            res = requests.get(forecast_url)
            data = res.json()

            if res.status_code == 200:
                weather = {
                    "city": city.title(),
                    "description": data["list"][0]["weather"][0]["description"].title(),
                    "temperature": data["list"][0]["main"]["temp"]
                }

                # Prepare chart data (next 8 timestamps = approx 24 hours)
                chart_data = [
                    {
                        "time": item["dt_txt"][11:16],
                        "temp": item["main"]["temp"]
                    } for item in data["list"][:8]
                ]
            else:
                error = "Weather data not available."
        else:
            error = "City not found."

    return render_template("weather.html", weather=weather, error=error, chart_data=chart_data)

if __name__ == "__main__":
    app.run(debug=True)
