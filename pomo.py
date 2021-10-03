import asyncio

async def focus(minutes, message, studyActive):
    seconds = minutes * 60
    studyActive[message.author] = seconds
    if (minutes == 1):
      focusMsg = str(minutes) + " minute"
    else:
      focusMsg = str(minutes) + " minutes"
    await message.channel.send("Alright, see you in " + focusMsg + 
      ".  Good luck on your work~")
    while seconds:
      await asyncio.sleep(1)
      seconds -= 1
      studyActive[message.author] = seconds
      print(seconds)
    studyActive.pop(message.author)
    await message.channel.send("Good job, {}! Now go grab a cookie and relax.".format(message.author.mention))

async def relax(minutes, message, relaxActive):
    seconds = minutes * 60
    if (minutes == 1):
      focusMsg = str(minutes) + " minute"
    else:
      focusMsg = str(minutes) + " minutes"
    await message.channel.send("Alright, see you in " + focusMsg + 
      ".  Have a good break~")
    while seconds:
      await asyncio.sleep(1)
      relaxActive[message.author] = seconds
      seconds -= 1
      print(seconds)
    relaxActive.pop(message.author)
    await message.channel.send("Break's over, {}! Get back to work!".format(message.author.mention))
