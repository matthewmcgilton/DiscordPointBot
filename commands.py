import json
import os
import pymongo
from settings import message_reward_weight

#Help command which shows all commands
async def help(msg):
    await msg.channel.send(f"Commands:\n- $help\n- $balance\n- $top")
    await msg.channel.send(f"Games:\n- $coinflip")

#Command which allows users to check their balance
async def balance(msg, database):
    #Searches the user id in the server collection
    collection = database[str(msg.guild.id)]
    query = {"_id": msg.author.id}
    search = list(collection.find(query)) #Cursor object saved as a list

    #If the user wasn't found create one and return 0 points, otherwise return points of existing user
    if len(search) == 0:
        await msg.channel.send(f"{msg.author.name}, you have 0 points")
        collection.insert_one({"_id": msg.author.id, "name": msg.author.name, "points": 0})
    else:
        await msg.channel.send(f"{search[0]['name']}, you have {search[0]['points']} points")

#Command which displays the top 3 users of the server.
async def top_users(msg, database):
    #From collection, sort by points
    collection = database[str(msg.guild.id)]
    search = list(collection.find().sort("points", -1))
    
    #TODO make this an embed rather than just printing 3 messages
    i = 1
    for user in search:
        await msg.channel.send(f"{i}. {user['name']} has {user['points']} points")
        i += 1

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