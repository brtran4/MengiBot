import requests
baseURL = "http://api.openweathermap.org/data/2.5/weather?"
APIKEY = "8b7f86aa407415a8493c1c4f8926ac64"

def weather(city):
  cityName = city
  completeURL = baseURL +  "q=" + cityName + "&appid=" + APIKEY
  print(completeURL)
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
      ftemp= "\nTemperature(F): " + str(int(currentTempCelsius) * (9/5) + 32) + "°F"
      ctemp = "\nTemperature(C): " + str(currentTempCelsius) + "°C"
      humidity ="\nHumidity(%): " + str(currentHumidity) + "%"
      pressure ="\nAtmospheric Pressure(hPa): " + str(currentPressure) + " hPa"

      return title + description + ftemp + ctemp + humidity + pressure
  else:
      return "City not found."