import discord
import commands
import games

#Initial setup
prefix = '$'
intents = discord.Intents.all()

token = ""
client = discord.Client(intents=intents)

#Events
@client.event #decorator function
async def on_ready():
    print(f"Bot logged in as {client.user}")
    
@client.event
async def on_message(msg):
    #Check to ignore bot messages
    if msg.author != client.user:
        #Commands/games
        if msg.content.lower().startswith("$coinflip"):
            await games.coinflip(msg, client)
        elif msg.content.lower().startswith("$top"):
            await commands.top_users(msg, client)
        elif msg.content.lower().startswith("$balance"):
            await commands.balance(msg)
        else:
            await commands.add_points(msg)

#Start
client.run(token)