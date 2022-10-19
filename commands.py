import json
import os

#Help command which shows all commands
async def help(msg):
    pass

#Command which allows users to check their balance
async def balance(msg):
    with open(f"{os.path.dirname(__file__)}/Servers/{msg.guild.id}.txt") as file:
        data = json.loads(file.read())

    await msg.channel.send(f"You have {data[str(msg.author.id)]} points")

#Command which displays the top 3 users of the server.
async def top_users(msg, client):
    #Opens the file for the server
    with open(f"{os.path.dirname(__file__)}/Servers/{msg.guild.id}.txt") as file:
        data = json.loads(file.read())

    #
    #TODO make this an embed rather than just printing 3 messages
    #
    #Function to iterate through first 3 values of the dict
    for i in sorted(data.values(), reverse=True)[:3]:
        userid = (list(data.keys())[list(data.values()).index(i)])
        username = await client.fetch_user(int(userid))
        await msg.channel.send(f"{username} has {i} points")

#Command which adds points to a user's balance
async def add_points(msg):
    #Set important values
    author = str(msg.author.id)
    amount = len(msg.content)
    server = str(msg.guild.id)
    path = f"{os.path.dirname(__file__)}/Servers/{server}.txt"

    #If the server doesn't already exist, create a file for it
    if not os.path.exists(path):
        file = open(path, "a")
        file.write("{}")
        file.close
    
    #Open the file of the server
    with open(path) as file:
        data = json.loads(file.read())

    #Checks if the user is on the server
    if author not in data:
        data[author] = amount
    else:
        data[author] += amount
    
    #Saves the changes to the file
    with open(path, 'w') as file:
        json.dump(data, file)