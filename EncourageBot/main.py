import os
import discord
import requests 
import json
import random
from replit import db

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

def get_quote() :
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote
  
client = discord.Client(intents=intent)

sad_words = ["sad" , "unhappy" , "depressed" , "miserable" , "depressing"]

starter_encouragements = [
  "Cheer up!" ,
   "Hang in there" ,
   "You are a great person" ,
   "Rise and SHINE!"
  ]

def update_encouragements(encouraging_message) :
  if "encouragements" in db.keys() :
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else :
     db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index :
     del encouragements[index]
     db["encouragements"] = encouragements
 
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return

  if msg.startswith('$hello'):
    await message.channel.send('HELLO!')

  if msg.startswith('$new') :
    encouraging_message = msg.split("$new " ,1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])

  if any(word in msg for word in sad_words) :
    await message.channel.send(random.choice(options))

  if msg.startswith("del") :
    encouragements= [] 
    if "encouragements" in db.keys() :
     index = int(msg.split("$del" , 1)[1])
     delete_encouragement(index)
     encouragements = db["encouragements"]
     await message.channel.send(encouragements)

Keep_Alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)
