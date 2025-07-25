import requests
import tkinter as tk
from tkinter import messagebox
from urllib.parse import quote_plus

API_KEY = "OAc4qpQmG3xu1A9t6Nam1lvraWutEM9f"  # Your AccuWeather API Key

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        # Step 1: Get location key
        city_encoded = quote_plus(city)  # URL encode the city name
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city_encoded}"
        location_response = requests.get(location_url).json()

        if not location_response:
            messagebox.showerror("Error", "City not found.")
            return

        location_key = location_response[0]['Key']
        city_name = location_response[0]['LocalizedName']

        # Step 2: Get current conditions
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true"
        weather_response = requests.get(weather_url).json()

        if not weather_response:
            messagebox.showerror("Error", "Could not retrieve weather data.")
            return

        weather_data = weather_response[0]
        output = f"--- Current Weather in {city_name} ---\n"
        output += f"Temperature: {weather_data['Temperature']['Metric']['Value']} °C\n"
        output += f"Weather: {weather_data['WeatherText']}\n"
        output += f"Humidity: {weather_data['RelativeHumidity']}%\n"
        output += f"Wind Speed: {weather_data['Wind']['Speed']['Metric']['Value']} km/h\n"

        result_label.config(text=output)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Network error occurred: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# GUI Setup
p = tk.Tk()
p.title("Weather Forecasting App")
p.geometry("500x400")

tk.Label(p, text="Enter City:", font=("Arial", 15)).pack(pady=5)
city_entry = tk.Entry(p, width=30, font=("Arial", 12))
city_entry.pack(pady=5)

tk.Button(p, text="Get Weather", command=get_weather, font=("Arial", 15)).pack(pady=12)

result_label = tk.Label(p, text="", font=("Courier", 10), justify="left")
result_label.pack(padx=12, pady=12)

p.mainloop()
