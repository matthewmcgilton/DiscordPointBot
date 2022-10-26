import random
import discord

#Coinflip game which doubles the users bet if they guess correctly
async def coinflip(msg, database):
    #Start creating the message
    embed = discord.Embed(title="Coinflip Result", color=0x81c38a)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1031822902959550534/7a3a4c9ace0dcd545f79a0a3892526ee.webp?size=80")

    #Check to see if command is properly formatted e.g. $flip 500 up/down
    command = msg.content.lower().split(" ")
    if len(command) != 3:
        embed.add_field(name="Error", value="Command must be formatted $flip <amount> <up/down>", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Check to see if bet is an int
    try:
        int(command[1])
    except:
        embed.add_field(name="Error", value="Please enter a valid number to bet", inline=False)
        await msg.channel.send(embed=embed)
        return False

    #Check to see if bet is larger than 0
    if int(command[1]) <= 0:
            embed.add_field(name="Error", value="Please bet a value above 0", inline=False)
            await msg.channel.send(embed=embed)
            return False
    
    #Check to see if bet type is up or down
    if command[2] != "up" and command[2] != "down":
        embed.add_field(name="Error", value="Please either bet up or down", inline=False)
        await msg.channel.send(embed=embed)
        return False
    
    amount = int(command[1])
    bet = command[2]

    #Search for user in the server's collection
    collection = database[str(msg.guild.id)]
    query = {"_id": msg.author.id}
    search = list(collection.find(query))

    #If user not found, make one and tell them they don't have enough to bet
    if len(search) == 0:
        collection.insert_one({"_id": msg.author.id, "name": msg.author.name, "points": 0})
        embed.add_field(name="Error", value="You don't have enough to bet", inline=False)
        await msg.channel.send(embed=embed)
        return False
    
    #Otherwise check the existing user's points vs the amount they want to bet
    if search[0]['points'] < amount:
        embed.add_field(name="Error", value="You don't have enough to bet", inline=False)
        await msg.channel.send(embed=embed)
        return False
    
    #All checks passed, complete the flip, 0 for down, 1 for up
    result = "down" if random.randint(0, 1) == 0 else "up"
    new_balance = 0
    if bet == result:
        new_balance = search[0]['points']+amount
        embed.add_field(name="Congrats!", value=f"The coin landed {result} and you won {amount} points!", inline=False)
        collection.update_one(query, {"$set": {"points": new_balance}})
    else:
        new_balance = search[0]['points']-amount
        embed.add_field(name="Sorry!", value=f"The coin landed {result} and you lost {amount} points", inline=False)
        collection.update_one(query, {"$set": {"points": new_balance}})

    embed.set_footer(text=f"Your balance is now {new_balance} points")
    await msg.channel.send(embed=embed)