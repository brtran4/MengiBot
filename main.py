import discord # discord documentation runs on events
import os # takes private token and passes to the client
import random
import math
from replit import db # uses repl.it database
from keep_alive import keep_alive
from weather import weather
from encouragements import updateEncouragements
from encouragements import starterEncouragements
from encouragements import deleteEncouragment
from encouragements import getQuote
from encouragements import sadWords
from pomo import focus
from pomo import relax

client = discord.Client()

studyActive = {}
relaxActive = {}


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
    await message.channel.send(weather(cityName))

  if msg.startswith("!focus"):
    if message.author in studyActive:
      await message.channel.send("You still have {} minutes left, {}".format(math.ceil(studyActive[message.author]/60), message.author.mention)) 
      return
    minutes = int(msg.split("!focus ", 1)[1])
    await focus(minutes, message, studyActive)
  
  if msg.startswith("!relax"):
    if message.author in relaxActive:
      await message.channel.send("You still have {} minutes left, {}".format(math.ceil(relaxActive[message.author]/60), message.author.mention)) 
      return
    minutes = int(msg.split("!relax ", 1)[1])
    await relax(minutes, message, relaxActive)

keep_alive()
client.run(os.getenv("TOKEN"))