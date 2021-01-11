import discord #discord documentation runs on events
import os # takes private token and passes to the client

client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith("!hello"):
    await message.channel.send("Hello!") #send message to channel

client.run(os.getenv("TOKEN"))