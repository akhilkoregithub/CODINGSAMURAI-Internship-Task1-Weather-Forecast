import tkinter as tk
import requests
import json

# API key from OpenWeatherMap
API_KEY = 'd5c43971261fa1b7542f83e069fac82f'

def convert_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

def convert_to_fahrenheit(temp_kelvin):
    return (temp_kelvin - 273.15) * 9/5 + 32

def get_weather_data(location, units='metric'):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': location, 'appid': API_KEY, 'units': units}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception if the request is not successful
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def display_weather_info(weather_data, units='metric'):
    if weather_data:
        main_info = weather_data['main']
        weather_info = weather_data['weather'][0]
        wind_info = weather_data['wind']

        temperature_unit = '°C' if units == 'Celsius' else '°F'
        temperature = main_info['temp']
        humidity = main_info['humidity']
        wind_speed = wind_info['speed']
        description = weather_info['description']

        result_text.set(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:\n"
                        f"Temperature: {temperature:.2f} {temperature_unit}\n"
                        f"Humidity: {humidity}%\n"
                        f"Wind Speed: {wind_speed} m/s\n"
                        f"Conditions: {description.capitalize()}")
    else:
        result_text.set("No weather data available for the specified location.")

def fetch_weather():
    location = location_entry.get()
    units = units_var.get()

    if units not in ['Celsius', 'Fahrenheit']:
        units = 'Celsius'  # Default to Celsius 

    weather_units = 'metric' if units == 'Celsius' else 'imperial'
    weather_data = get_weather_data(location, weather_units)
    display_weather_info(weather_data, units)

# main application window
root = tk.Tk()
root.title("Weather Forecast")

# Calculate the x and y coordinates to center the window
window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and configure GUI elements
location_label = tk.Label(root, text="Enter a city or location:")
location_entry = tk.Entry(root, width=23, highlightthickness=1, highlightbackground="black")  # Add border
units_label = tk.Label(root, text="Choose temperature units:")
units_var = tk.StringVar(value="Celsius")
units_menu = tk.OptionMenu(root, units_var, "Celsius", "Fahrenheit")
units_menu.config(width=18, highlightthickness=1, highlightbackground="black", bg="lightpink")  # Add border and set background color
fetch_button = tk.Button(root, width=20, text="Fetch Weather", command=fetch_weather, highlightthickness=1, highlightbackground="black", bg="lightgreen")  # Add border and set background color
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)

# Place GUI elements using grid layout
location_label.grid(row=0, column=0, padx=10, pady=5)
location_entry.grid(row=1, column=0, padx=10, pady=5)
units_label.grid(row=2, column=0, padx=10, pady=5)
units_menu.grid(row=3, column=0, padx=10, pady=5)
fetch_button.grid(row=4, column=0, padx=10, pady=5)
result_label.grid(row=5, column=0, padx=10, pady=5)

# Center the middle column (column 0) to align widgets horizontally in the middle
root.grid_columnconfigure(0, weight=1)

# Tkinter main loop
root.mainloop()
