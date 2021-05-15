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

client = commands.Bot(command_prefix=".")

class BotData:
    def __init__(self):
        self.counting_channel = None

botdata = BotData()

@client.event
async def on_ready():
    print("Bot ready!")

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


# @client.command()
# async def test(ctx):
#     embed = discord.Embed(color = discord.Color.blue())
#     width = 7
#     height = 7

#     await ctx.send(":white_large_square:" * width)
#     for i in range(height):
#         await ctx.send(":white_large_square:" + ('          ' * width) + ":white_large_square:")
#         if i == 4:
#             pass
#     await ctx.send(":white_large_square:" * width)

#     embed.add_field(name = "\u200B", value="\u200B")

@client.command(aliases=["counting"])
async def counting_channel(ctx, channel_name = None):
    if channel_name != None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                botdata.counting_channel = channel
                await ctx.channel.send(f"Counting channel has been set to: {channel.name}")
                await channel.send(f"This is your counting channel")
                return channel_name

    else:
        await ctx.channel.send("You didnt configure a counting channel")


# @client.event
# async def on_message(message:discord.Message):
#     channel = client.get_channel(id = 830233837694877729)
#     if message.channel.id == 830233837694877729 and message.guild.id == 830233837119471637:
#         if not message.author.bot:
#             pass
#         else:
#             pass
            
                

                # change the order of the coderst)


                    # n = first + 1
                    # print(n)
                    # print("number to be entered", n)
                    # next_number = str(n)
                    # if msg.content == next_number:
                    #     first += 1
                    #     print(first)
                    #     print("Passed!")
                    #     print(f"Next number : {first + 1}")
                        
                        
                            
                    # else:
                    #     pass
        
# @client.command()
# async def test(ctx):
#     await ctx.send("y or n")
#     def check(msg):
#         return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y","n"]

#     msg = await client.wait_for("message",check=check)
#     if msg.content.lower() == "y":
#         await ctx.send("You said yes")
#     if msg.content.lower() == "n":
#         await ctx.send("You said no")

# @client.event
# async def on_message(message):
#     if message.content.startswith(".greet"):
#         channel = message.channel
#         await message.channel.send('say Hello')

#         def check(m):
#             return m.content == "hello" and m.channel == channel
        
#         msg = await client.wait_for('message', check=check)
#         await channel.send(f"Hello {msg.author}")
    
#     await client.process_commands(message)

@client.event
async def on_message(message):  
    channel = client.get_channel(830233837694877729)
    if not message.author.bot:
        if channel is None:
            print("cant find channel")
            return
        msg = await channel.fetch_message(channel.last_message.id)
        await message.channel.send(f"Last message in channel {channel.name} sent by {msg.author.name} and contains {msg.content}")

    # if message.channel.id == channel and message.guild.id == 830233837119471637:
        
            




@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)


client.run('TOKEN')
