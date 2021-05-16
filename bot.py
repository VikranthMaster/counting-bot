from re import I
import discord
from discord.ext import commands
import sqlite3
from discord.flags import MessageFlags
import pypokedex
import urllib3
from io import BytesIO
import PIL.Image, PIL.ImageTk
import sys
import os.path
from PIL import Image
import asyncio
import time

client = commands.Bot(command_prefix=".")
client.remove_command('help')

class BotData:
    def __init__(self):
        self.counting_channel = None

client1 = discord.Client()

botdata = BotData()


@client.event
async def on_ready():
    print(f"{client.user} ready!")


@client.command(aliases=["counting", "set_counting_channel"])
async def counting_channel(ctx, channel: discord.TextChannel):
    if channel == None:
        await ctx.send("The channel you have provided is incorrect")
    else:
        botdata.counting_channel = channel
        embed = discord.Embed(color = discord.Color.blue())
        embed.add_field(name = f"**__Welcome to Counting Bot__ :robot:**", value = f"So you have choosen to start your counting in {channel} good luck !! :partying_face:", inline = False)
        embed.add_field(name = f"**__Rules__**", value = f"Rules are pretty simple\n **``1)Do not break the chain\n2)The message u send should be an integer\n3)One person cant send two messages at a time\n``**")
        embed.add_field(name = f"**__Disclaimer__ :octagonal_sign:**", value = f"If you break any one of the rule, you and your server memebers have to start the game from the beginning so be mindful of what are about to send")
        embed.set_footer(text="Remember you can always change the channel")
        await ctx.send(embed=embed)

        embed = discord.Embed(color = discord.Color.blue())
        embed.add_field(name = f"**Channel**", value = f"This is your counting channel...**WAIT BEFORE THIS MESSAGE DELETES and** **Start the count from ``1``**",inline=False)
        embed.set_footer(text=" :partying_face: Good luck !")
        something = await channel.send(embed=embed)
        await asyncio.sleep(10)
        await something.delete()
        # print(botdata.counting_channel.id)


@client.listen()
async def on_message(message):
    async def clear(ctx, amount):
        await ctx.channel.purge(limit = amount + 1)

    channel = client.get_channel(botdata.counting_channel.id)

    if message.channel != channel or message.author.bot:
        #wrong channel or author is a bot
        return

    history = await channel.history().flatten()
    latest_messages = await channel.history(limit=2).flatten()
    lastest_message2 = latest_messages[1].author
    lastest_message1 = latest_messages[0].author
    if not all(msg.content.isdigit() for msg in latest_messages):
        #not all the messages are an int
        return

    if not message.content.isdigit():
        #input message is not an int
        embed = discord.Embed(color= discord.Color.blue())
        embed.add_field(name=f"**Message not a integer :x:**", value = f":bangbang: {lastest_message1.mention} Dude it should be a number not a integer :bangbang:")
        await channel.send(embed=embed)
        await asyncio.sleep(20)
        await channel.purge(limit=1)
        await clear(message,100000000)

    if lastest_message1 != lastest_message2:
        if (int(latest_messages[0].content) - int(latest_messages[1].content)) == 1:
            print("looking good")
        else:   
            print("Number squence break")
            embed = discord.Embed(color = discord.Color.blue())
            embed.add_field(name = f"**Breaking of chain :x: **", value = f":bangbang: The chain was broken by {str(latest_messages[0].author.mention)} at {str(latest_messages[1].content)} :bangbang:")
            embed.set_thumbnail(url = f"{latest_messages[0].author.avatar_url}")
            await channel.send(embed = embed)
            await asyncio.sleep(20)
            await clear(message,1000000000)

    else:
        embed = discord.Embed(color = discord.Color.blue())
        embed.add_field(name = f"**Repeated User :x: **", value = f":bangbang: {lastest_message1.mention} Oh-oh dude what did you do, you just ruined the perfect going chain by sending your message twice :confused: :bangbang:")
        await channel.send(embed=embed)
        await asyncio.sleep(20)
        await clear(message,10000000000)

        # history = await channel.history().flatten()
        # guild = message.guild
        # if lastest_message1 == lastest_message2:
        #     print("User repeated")
        #     await clear(message,int(latest_messages[0].content))

@client.command()
async def help(ctx):
    embed = discord.Embed(color = discord.Color.blue())
    embed.add_field(name = f"**__Welcome to counting bot__ :robot:**", value = f"Hello {ctx.author.name} :wave: Thanks for adding me to your server :blush: \n\nSo..basically i have only one command which is ``.set_counting_channel [channel]``. That channel becomes your counting channel for this server\n\n You will get all the information after you type the command\n\nGood luck :partying_face: and Happy Counting !!", inline = False)
    await ctx.send(embed=embed)

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)


client.run('TOKEN') 
