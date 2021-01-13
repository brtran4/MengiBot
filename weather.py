import requests
import os
baseURL = "http://api.openweathermap.org/data/2.5/weather?"

def weather(city):
  cityName = city
  completeURL = baseURL +  "q=" + cityName + "&appid=" + os.getenv("APIKEY")
  response = requests.get(completeURL)
  x = response.json()

  if x["cod"] != "404": # error checking if city is valid
      y = x["main"]
      currentTemp = y["temp"]
      currentTempCelsius = str(round(currentTemp - 273.15))
      currentPressure = y["pressure"]
      currentHumidity = y["humidity"]
      z = x["weather"]
      weatherDescription = z[0]["description"]

      title = "Current weather in " + cityName + ":"
      description = "\nDescripition: " + str(weatherDescription)
      ftemp= "\nTemperature(F): " + str(round(int(currentTempCelsius) * (9/5) + 32)) + "°F"
      ctemp = "\nTemperature(C): " + str(currentTempCelsius) + "°C"
      humidity ="\nHumidity(%): " + str(currentHumidity) + "%"
      pressure ="\nAtmospheric Pressure(hPa): " + str(currentPressure) + " hPa"

      return title + description + ftemp + ctemp + humidity + pressure
  else:
      return "City not found."