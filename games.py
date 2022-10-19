import os
import json
import random

#Coinflip game which doubles the users bet if they guess correctly
async def coinflip(msg, client):
    #Splits it in to a list of components E.g. ["$coinflip", "heads/tails", "value"]
    message = msg.content.split(" ")
    author = str(msg.author.id)

    #Checks to make sure only necessary components in the command
    if(len(message) != 3):
        await msg.channel.send("""Please ensure that you formatted the command properly
                                  \n$coinflip heads/tails amount""")
        return False
    
    #Checks to make sure only heads or tails picked
    if(message[1] != "heads" and message[1] != "tails"):
        await msg.channel.send("Make sure you entered heads or tails as your choice")
        return False

    #Checks to make sure bet is a number and is larger than 0
    try:
        if(int(message[2]) <= 0):
            await msg.channel.send("Make sure you bet more than 0 points")
            return False
    except ValueError:
        await msg.channel.send("Make sure you entered a number to bet")
        return False

    #Opens the file for the server
    path = f"{os.path.dirname(__file__)}/Servers/{msg.guild.id}.txt"
    with open(path) as file:
        data = json.loads(file.read())
    
    if author not in data:
        await msg.channel.send("Your bet exceeded your current balance")
        print("POG")
        return False

    if data[author] < int(message[2]):
        await msg.channel.send("Your bet exceeded your current balance")
        print("POasdG")
        return False
    
    choice = "heads" if random.randint(0, 1) == 0 else "tails"
    if message[1] == choice:
        data[author] += int(message[2])
        await msg.channel.send(f"The coin landed on {choice}! You won {int(message[2])*2}")
    else:
        data[author] -= int(message[2])
        await msg.channel.send(f"The coin landed on {choice}! You lost {int(message[2])}")
    
    with open(path, 'w') as file:
        json.dump(data, file)