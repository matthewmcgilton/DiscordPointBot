import discord
import commands
import games
import pymongo
from settings import Settings

#Discord setup
prefix = '$'
intents = discord.Intents.all()
token = Settings().BOT_TOKEN
client = discord.Client(intents=intents)

#MongoDB setup
myclient = pymongo.MongoClient(Settings().MONGO_ADDRESS)
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
        elif msg.content.lower().startswith("$send"):
            await commands.transfer(msg, database)
        else:
            await commands.add_points(msg, database)

#Start
client.run(token)