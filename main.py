import discord
import commands
import games
import pymongo

#Discord setup
prefix = '$'
intents = discord.Intents.all()
token = "YOUR TOKEN HERE"
client = discord.Client(intents=intents)

#MongoDB setup
myclient = pymongo.MongoClient("YOUR DATABASE ADDRESS HERE")
database = myclient["DiscordBot"]

#Events
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    
@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith("$top"):
            await commands.top_users(msg, database)
        elif msg.content.lower().startswith("$balance") or msg.content.lower().startswith("$bal"):
            await commands.balance(msg, database)
        elif msg.content.lower().startswith("$help"):
            await commands.help(msg)
        elif msg.content.lower().startswith("$flip"):
            await games.coinflip(msg, database)
        else:
            await commands.add_points(msg, database)

#Start
client.run(token)