import discord
import random
from settings import message_reward_weight, jackpot_amount, jackpot_odds

#Help command which shows all commands
async def help(msg):
    embed = discord.Embed(title="Point Bot's Commands", color=0x81c38a)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1031822902959550534/7a3a4c9ace0dcd545f79a0a3892526ee.webp?size=80")
    embed.add_field(name="$help", value="Shows a list of all the bot's commands", inline=False)
    embed.add_field(name="$balance OR $bal", value="Shows your current point balance", inline=False)
    embed.add_field(name="$top", value="Shows the top 3 ranked users on the server", inline=False)
    embed.add_field(name="$flip <amount> <up/down>", value="Allows you to bet on the outcome of a coin to double your bet", inline=False)
    embed.add_field(name="$send <amount> <@user>", value="Allows you to send points to other server members", inline=False)
    await msg.channel.send(embed=embed)

#Command which allows users to send points to another user in the server
async def transfer(msg, database):
    #Start creating the message
    embed = discord.Embed(title="Transfer Points", color=0x81c38a)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1031822902959550534/7a3a4c9ace0dcd545f79a0a3892526ee.webp?size=80")

    #Check to see if command is properly formatted e.g. $send 500 @user
    command = msg.content.lower().split(" ")
    if len(command) != 3:
        embed.add_field(name="Error", value="Command must be formatted $send <amount> <@user>", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Check to see if bet is an int
    try:
        int(command[1])
    except:
        embed.add_field(name="Error", value="Please enter a valid number to send", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Check to see if bet is larger than 0
    if int(command[1]) <= 0:
            embed.add_field(name="Error", value="Please send an amount over 0", inline=False)
            await msg.channel.send(embed=embed)
            return False

    amount = int(command[1])
    reciever_id = int(command[2][2:-1])

    #Check to see if given ID exists on the server
    if msg.guild.get_member(reciever_id) is None:
        embed.add_field(name="Error", value="User given doesn't exist", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Search for sender in the server's collection
    collection = database[str(msg.guild.id)]
    query_sender = {"_id": msg.author.id}
    search_sender = list(collection.find(query_sender))

    #If sender not found, make one and tell them they don't have enough to send
    if len(search_sender) == 0:
        collection.insert_one({"_id": msg.author.id, "name": msg.author.name, "points": 0})
        embed.add_field(name="Error", value="You don't have enough to send", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Check the existing user's points vs the amount they want to send
    if search_sender[0]['points'] < amount:
        embed.add_field(name="Error", value="You don't have enough to send", inline=False)
        await msg.channel.send(embed=embed)
        return False
    
    #Check if sender isn't the same user as the reciever
    if(search_sender[0]['_id'] == reciever_id):
        embed.add_field(name="Error", value="You may not send points to yourself", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Update sender
    collection.update_one(query_sender, {"$set": {"points": search_sender[0]['points']-amount}})

    #Search for reciever in the server's collection
    query_reciever = {"_id": reciever_id}
    search_reciever = list(collection.find(query_reciever))

    #If reciever not found create one with given amount, otherwise update existing users balance
    if len(search_reciever) == 0:
        collection.insert_one({"_id": reciever_id, "name": msg.guild.get_member(reciever_id).name, "points": amount})
    else:
        collection.update_one(query_reciever, {"$set": {"points": search_reciever[0]['points']+amount}})

    embed.add_field(name="Sent", value=f"You sent {amount} points to {msg.guild.get_member(reciever_id)}", inline=False)
    embed.set_footer(text=f"Your balance is now {search_sender[0]['points']-amount} points")
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
    
    #Iterate through search to add top 3 users to the embed
    total_server_points = 0
    for index, user in enumerate(search):
        total_server_points += user['points']
        if index < 3:
            embed.add_field(name=f"{index+1}. {user['name']}", value=f"{user['points']} points", inline=False)
        if index == 0:
            embed.set_thumbnail(url=msg.guild.get_member(user["_id"]).avatar)

    #Send the embed
    embed.set_footer(text=f"The server has a total of {total_server_points} points in circulation")
    await msg.channel.send(embed=embed)

#Command which adds points to a user's balance
async def add_points(msg, database):
    #Searches the user id in the server collection
    collection = database[str(msg.guild.id)]
    query = {"_id": msg.author.id}
    search = list(collection.find(query)) #Cursor object saved as a list
    amount = 0

    #Roll for user to win the jackpot
    if random.randint(1, 1000) <= jackpot_odds:
        amount = jackpot_amount
        await msg.channel.send(f"Congrats! You won the {(jackpot_odds/1000)*100}% jackpot worth {jackpot_amount} points!")
    else:
        amount = len(msg.content) * message_reward_weight

    #If the user wasn't found create one, otherwise add points to existing user
    if len(search) == 0:
        #Point amount is based on length of message multiplied by the reward weight setting
        collection.insert_one({"_id": msg.author.id, "name": msg.author.name, "points": amount})
        print(f"""New Event: New User\nServer: {msg.guild.id}\nUserID: {msg.author.id}\nUserName: {msg.author.name}\nPoints: {amount}\n==""")
    else:
        collection.update_one(query, {"$set": {"points": search[0]['points'] + amount}})
        print(f"""New Event: Add Points\nServer: {msg.guild.id}\nUserID: {msg.author.id}\nUserName: {msg.author.name}\nPoints: {amount}\n==""")