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

client = commands.Bot(command_prefix=".")

class BotData:
    def __init__(self):
        self.counting_channel = None

client1 = discord.Client()

botdata = BotData()

@client.event
async def on_ready():
    print(f"{client.user} ready!")

@client.command(aliases=["poke","pokemon","p","about"])
async def find(ctx,*,pokemon_name):
    pokemon = pypokedex.get(name=pokemon_name)
    http = urllib3.PoolManager()
    response = http.request('GET', pokemon.sprites.front.get('default'))
    image = PIL.Image.open(BytesIO(response.data))
    img = image.save("pokemon.png")
    await ctx.send(f"{pokemon_name} found!")
    with open("pokemon.png","rb") as fp:
        print("All is working good")

    type_pokemon = pokemon.types
    res = str(type_pokemon)[1:-1]

    filePath = discord.File("C:/Users/shankar/OneDrive/Desktop/shanmukha/Python/Discord/pokemon.png", filename = "pokemon.png")

    embed = discord.Embed(color = discord.Color.blue())
    embed.add_field(name = f"**__{pokemon.name}__**", value = f"Showing Stats for {pokemon.name}", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Pokedex number**: ``{pokemon.dex}``", inline=False)
    embed.add_field(name = f"\u200b", value = f"**Types**: ``{res}``",inline=False)
    embed.add_field(name = f"\u200b",value = f"**HP**: ``{pokemon.base_stats.hp}``", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Attack**: ``{pokemon.base_stats.attack}``", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Defence**: ``{pokemon.base_stats.defense}``", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Special Attack**: ``{pokemon.base_stats.sp_atk}``", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Special Defence**: ``{pokemon.base_stats.sp_def}``", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Height**: ``{pokemon.height*10}``", inline=False)
    embed.add_field(name = f"\u200b",value = f"**Weight**: ``{pokemon.weight/10}``", inline=False)

    embed.set_image(url = "attachment://pokemon.png")
    embed.set_thumbnail(url = ctx.author.avatar_url)
    await ctx.send(file = filePath,embed=embed)

@client.command(aliases=["counting"])
async def counting_channel(ctx, channel: discord.TextChannel):
    if channel == None:
        await ctx.send("The channel you have provided is incorrect")
    else:
        botdata.counting_channel = channel
        await ctx.channel.send(f"Counting channel has been set to {channel.name}")
        await channel.send("This is ur counting channel")

    if channel != None:
        if channel.name == channel:
            botdata.counting_channel = channel
            await ctx.channel.send(f"Counting channel has been set to: {channel.name}")
            await channel.send(f"This is your counting channel")

    else:
        await ctx.channel.send("You didnt configure a counting channel")


@client.listen()
async def on_message(message):
    async def clear(ctx, amount):
        await ctx.channel.purge(limit = amount + 1)

    channel = client.get_channel(843068576936230912)
    if message.channel != channel or message.author.bot:
        #wrong channel or author is a bot
        return

    latest_messages = await channel.history(limit=2).flatten()
    lastest_message2 = latest_messages[1].author
    lastest_message1 = latest_messages[0].author
    if not all(msg.content.isdigit() for msg in latest_messages):
        #not all the messages are an int
        return

    if not message.content.isdigit():
        #input message is not an int
        await clear(message,int(latest_messages[0].content))

    if lastest_message1 != lastest_message2:
        if (int(latest_messages[0].content) - int(latest_messages[1].content)) == 1:
            print("looking good")
        else:   
            print("Number squence break")
            await clear(message,int(latest_messages[0].content))
    else:
        print("User repeated...deleting")

        # history = await channel.history().flatten()
        # guild = message.guild
        # if lastest_message1 == lastest_message2:
        #     print("User repeated")
        #     await clear(message,int(latest_messages[0].content))


@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)


client.run('TOKEN') 
