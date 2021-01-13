import discord #discord documentation runs on events
import os # takes private token and passes to the client
import random
from replit import db # uses repl.it database
from keep_alive import keep_alive
from weather import weather
from encouragements import updateEncouragements
from encouragements import starterEncouragements
from encouragements import deleteEncouragment
from encouragements import getQuote
from encouragements import sadWords

client = discord.Client()

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