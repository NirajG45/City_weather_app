import tkinter as tk
import requests

API_KEY = "f82d429e6a4cb8fecadd760ca2c4a2ed"  # यहां अपनी OpenWeatherMap की key डालो

def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            result = f"Weather in {city}:\n{weather.capitalize()}\nTemperature: {temp}°C"
        else:
            result = f"Error: {data.get('message', 'City not found')}"

        result_label.config(text=result)
    except:
        result_label.config(text="Network error or invalid response.")

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("300x200")

tk.Label(root, text="Enter City Name:").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather).pack(pady=10)
result_label = tk.Label(root, text="", wraplength=250, justify="center")
result_label.pack(pady=10)

root.mainloop()
