import discord
import os
import requests
import json
import random
from replit import db
 
from stay_awake import stay_awake

# Client instance
client = discord.Client()

# sad words list
sad_words = ["sad", "depressed", "unhappy", "depressing", "unmotivated", "suicide"]

starter_encouragements = [
  "Cheer Up!",
  "Hang in there",
  "You are a great person / bot !"
]

if "responding" not in db.keys():
  db["responding"] = True 

# Function that returns quote from API
def get_quote():
    res = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(res.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']

    return quote

# This functions will update encouragements in the replit db
def update_encouragements(encouraging_msg):
  # Check for key in the database
  if "encouragements" in db.keys(): 
    encouragements = db["encouragements"]

    # An encouraging message added to db
    encouragements.append(encouraging_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_msg]


# delete an encouraging message
def del_encouragement(index):
  encouragements = db["encouragements"]

  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


# Called when bot is ready for use
@client.event
async def on_ready():
    print('Started as {0.user}'.format(client))


# Bot senses a message if message from bot do nothing
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    message = msg.content

    if message.startswith('$inspire'):
      quote = get_quote()
      await msg.channel.send(quote)
    
    if db["responding"]:
      options = starter_encouragements
    
      # Check whether specific key exits
      if "encouragements" in db.keys():
        options = options + db["encouragements"] 
      
      if any(word in message for word in sad_words):
        await msg.channel.send(random.choice(options))
    
    if message.startswith("$new"):
      encouraging_msg = message.split("$new ", 1)[1]
      update_encouragements(encouraging_msg)

      # Send users a message to verify message added
      await msg.channel.send("Encouraging message added!!")

    if message.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(message.split("$del", 1)[1])
        del_encouragement(index)

        encouragements = db["encouragements"]
        await msg.channel.send(encouragements)

    # Shows messages available in our database
    if message.startswith("$show"):
       if "encouragements" in db.keys():
         encouragements = db["encouragements"]

         await msg.channel.send(encouragements)


    # Whether bot will respond to sad messages or not
    if message.startswith("$responding"):
      value = message.split("$responding ", 1)[1]

      if value.lower() == "true":
        db["responding"] = True

        await msg.channel.send("Responding is on")
      else:
        db["responding"] = False
        
        await msg.channel.send("Responding is off")


stay_awake()

# To run the bot
client.run(os.getenv('DISCORD_TOKEN'))
