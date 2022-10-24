import json
import os
import pymongo
import discord
from settings import message_reward_weight

#Help command which shows all commands
async def help(msg):
    embed = discord.Embed(title="Point Bot's Commands", color=0x81c38a)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1031822902959550534/7a3a4c9ace0dcd545f79a0a3892526ee.webp?size=80")
    embed.add_field(name="$help", value="Shows a list of all the bot's commands", inline=False)
    embed.add_field(name="$balance OR $bal", value="Shows your current point balance", inline=False)
    embed.add_field(name="$top", value="Shows the top 3 ranked uers on the server", inline=False)
    await msg.channel.send(embed=embed)

#Command which allows users to check their balance
async def balance(msg, database):
    #Searches the user id in the server collection
    collection = database[str(msg.guild.id)]
    query = {"_id": msg.author.id}
    search = list(collection.find(query)) #Cursor object saved as a list

    #If the user wasn't found create one and return 0 points, otherwise return points of existing user
    if len(search) == 0:
        collection.insert_one({"_id": msg.author.id, "name": msg.author.name, "points": 0})
    
    #Create embed
    embed = discord.Embed(title=f"{msg.author.name}'s Balance", description=f"{search[0]['points']} points", color=0x81c38a)
    embed.set_thumbnail(url=msg.guild.get_member(search[0]["_id"]).avatar)

    await msg.channel.send(embed=embed)

#Command which displays the top 3 users of the server.
async def top_users(msg, database):
    #From collection, sort by points
    collection = database[str(msg.guild.id)]
    search = list(collection.find().sort("points", -1))

    #Create the embed
    embed = discord.Embed(title=f"{msg.guild.name}'s Leaderboard", color=0x81c38a)
    
    #Add a field for the top 3 users from the MongoDB search
    i = 1
    for user in search:
        embed.add_field(name=f"{i}. {user['name']}", value=f"{user['points']} points", inline=False)
        #Rank one user
        if i == 1:
            embed.set_thumbnail(url=msg.guild.get_member(user["_id"]).avatar)
        if i == 3:
            break
        i += 1

    #Send the embed
    await msg.channel.send(embed=embed)

#Command which adds points to a user's balance
async def add_points(msg, database):
    #Searches the user id in the server collection
    collection = database[str(msg.guild.id)]
    query = {"_id": msg.author.id}
    search = list(collection.find(query)) #Cursor object saved as a list

    #If the user wasn't found create one, otherwise add points to existing user
    if len(search) == 0:
        #Point amount is based on length of message multiplied by the reward weight setting
        amount = len(msg.content) * message_reward_weight
        collection.insert_one({"_id": msg.author.id, "name": msg.author.name, "points": amount})
        print(f"""New Event: New User\nServer: {msg.guild.id}\nUserID: {msg.author.id}\nUserName: {msg.author.name}\nPoints: {amount}\n==""")
    else:
        amount = search[0]['points'] + len(msg.content) * message_reward_weight
        collection.update_one(query, {"$set": {"points": amount} })
        print(f"""New Event: Add Points\nServer: {msg.guild.id}\nUserID: {msg.author.id}\nUserName: {msg.author.name}\nPoints: {amount}\n==""")