import discord
from discord import app_commands
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '>help':
        embed = discord.Embed(
            title="Help and Usage", description="Sir Count A Lot is a Discord counting bot.", color=discord.Color.from_rgb(0, 255, 4))
        embed.add_field(
            name='>setup', value='Sets up a counting channel in the current channel that the admin user is in.', inline=False)
        embed.add_field(
            name='>showstats', value='Shows stats of the current channel if it is setup.', inline=False)
        await message.channel.send(embed=embed)

    elif message.content == '>setup':
        if message.author.guild_permissions.administrator:
            with open('data', 'r') as ff:
                data = dict(json.load(ff))
            if str(message.guild.id) in data:
                if str(message.channel.id) in data[str(message.guild.id)]["channels"]:
                    await message.channel.send(f"Sir Count A Lot already added to #{message.channel.name}")
                else:
                    data[str(message.guild.id)]["channels"].update({
                        str(message.channel.id) : {
                            "Channel name": message.channel.name,
                            "Highest" : 0,
                            "Current" : 0,
                            "Previous" : 0
                        }
                    })
                    with open('data', 'w') as ff:
                        json.dump(data, ff)
                    await message.channel.send(f"Added Sir Count A Lot to check counting in #{message.channel.name}, start counting now!")
                    
            else:
                data.update({
                    str(message.guild.id): {
                        "Server Name": message.guild.name,
                        "channels": {
                            str(message.channel.id) : {
                                "Channel name": message.channel.name,
                                "Highest" : 0,
                                "Current" : 0,
                                "Previous" : 0
                            }
                        }
                    }
                })
                with open('data', 'w') as ff:
                    json.dump(data, ff)
                await message.channel.send(f"Added Sir Count A Lot to check counting in #{message.channel.name}, start counting now!")

        else:
            await message.channel.send("You do not have permission to do that!")
    
    elif message.content == '>showstats':
        
        await message.channel.send("You do not have permission to do that!")


    else:
        try:
            new = int(message.content)
            with open('data', 'r') as ff:
                data = dict(json.load(ff))
            if str(message.guild.id) in data:
                if str(message.channel.id) in data[str(message.guild.id)]["channels"]:
                    old  = data[str(message.guild.id)]["channels"][str(message.channel.id)]["Current"]
                    if data[str(message.guild.id)]["channels"][str(message.channel.id)]["Previous"] == message.author.id:
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Previous"] = 0
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Current"] = 0
                        await message.add_reaction("❌")
                        await message.channel.send(f"{message.author.mention} broke the chain. You cannot count twice in a row. Next number is 1")
                    elif old + 1 == new:
                        await message.add_reaction("✅")
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Current"] = new
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Highest"] = new
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Previous"] = message.author.id
                    else:
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Current"] = 0
                        data[str(message.guild.id)]["channels"][str(message.channel.id)]["Previous"] = 0
                        await message.add_reaction("❌")
                        await message.channel.send(f"{message.author.mention} broke the chain. Next number is 1")
                    with open('data', 'w') as ff:
                        json.dump(data, ff)
        except:
            pass

client.run(os.environ['DISCORD_TOKEN'])
