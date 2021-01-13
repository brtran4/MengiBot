import requests
import json
from replit import db # uses repl.it database

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