import discord #discord documentation runs on events
import os # takes private token and passes to the client
import requests # makes http requests
import json
import random
from replit import db # uses repl.it database
from keep_alive import keep_alive

client = discord.Client()


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
      pressure ="\nAtmospheric Pressure(hPa): " + str(currentPressure) + "hPa"

      return title + description + ftemp + ctemp + humidity + pressure
  else:
      return "City not found."




sadWords = ["sad", "depressed", "unhappy"]

starterEncouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  jsonData = json.loads(response.text)
  quote = jsonData[0]['q'] + " -" + jsonData[0]['a']
  return quote



def updateEncouragements(encouragingMessage):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouragingMessage)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouragingMessage]
  
def deleteEncouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index: # makes sure it is in the list
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if message.content.startswith("!hello"):
    await message.channel.send("Hello!") #send message to channel
  if message.content.startswith('!inspire'):
    await message.channel.send(getQuote())

  if db["responding"]:
    options = starterEncouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sadWords):
      await message.channel.send(random.choice(options))

  if msg.startswith("!new"):
    encouragingMessage = msg.split("!new ", 1)[1]
    updateEncouragements(encouragingMessage)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!del", 1)[1])
      deleteEncouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("!list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("!responding"):
    value = msg.split("!responding ", 1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("!weather"):
    cityName = msg.split("!weather ", 1)[1]
    print(cityName)
    await message.channel.send(weather(cityName))

keep_alive()
client.run(os.getenv("TOKEN"))