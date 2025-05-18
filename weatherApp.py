from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "f82d429e6a4cb8fecadd760ca2c4a2ed"  # this is my OpenWeatherMap API key for free use

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize()
            }
        else:
            error = data.get("message", "City not found or API error.")

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
