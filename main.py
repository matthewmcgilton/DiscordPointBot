import discord
import commands
import games
import pymongo

#Discord setup
prefix = '$'
intents = discord.Intents.all()
token = ""
client = discord.Client(intents=intents)

#MongoDB setup
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
database = myclient["DiscordBot"]

#Events
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    
@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith("$coinflip"):
            await games.coinflip(msg, database)
        elif msg.content.lower().startswith("$top"):
            await commands.top_users(msg, database)
        elif msg.content.lower().startswith("$balance"):
            await commands.balance(msg, database)
        elif msg.content.lower().startswith("$help"):
            await commands.help(msg)
        else:
            await commands.add_points(msg, database)

#Start
client.run(token)