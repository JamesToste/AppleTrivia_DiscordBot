import asyncio

import discord
import requests
from discord.ext import tasks, commands
import time

# Token for client login
TOKEN = ''
THREADS = []
WHITELIST = []
client = discord.Client()


# Main 'Apple Trivia' driver
async def appleTrivia(authr):
    # Embed message with all of the options
    embedAT = discord.Embed(title="Apple Trivia", description="Hello! What do you want to do?", color=0xFFFFFF)
    embedAT.add_field(name="\U00002753 option"
                      , value="Start a new trivia question"
                      , inline=False)

    embedAT.add_field(name="\U0000270F option"
                      , value="Edit the currently running trivia question"
                      , inline=False)

    embedAT.add_field(name="\U0000274C option"
                      , value="Close the currently running trivia question"
                      , inline=False)

    embedAT.add_field(name="\U0001F4C4 option"
                      , value="View details about the currently running trivia question"
                      , inline=False)

    # Send message to user
    msg = await authr.send(embed=embedAT)

    # Add reactions as the option buttons
    await msg.add_reaction('\U00002753')
    await msg.add_reaction('\U0000270F')
    await msg.add_reaction('\U0000274C')
    await msg.add_reaction('\U0001F4C4')



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('$help'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # DM detector for apple trivia
    if not message.guild:
        if "AT login" in message.content and message.author.id in WHITELIST:
            #await appleTrivia(message)

            apple_task = asyncio.create_task(appleTrivia(message.author))
            THREADS.append(apple_task)
            return

        elif "AT login" in message.content and message.author.id not in WHITELIST:
            print(message.author)
            await message.author.send("Unauthorized attempted access. Your Discord name has been recorded!")


# Looks for a raw reaction add since on_reaction_add can not scan DMChannel
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)

    # Avoids an error when a reaction is added to an old message sent before the bot was running
    if not channel:
        return

    message = await channel.fetch_message(payload.message_id)
    embed = message.embeds[0]

    user = client.get_user(payload.user_id)

    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U00002753' and payload.user_id in WHITELIST:
        embedAT = discord.Embed(title="Start a new question"
                                , description="What should the new trivia question be?"
                                , color=0xFFFFFF)

        await channel.send(embed=embedAT)

    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U0000270F' and payload.user_id in WHITELIST:
        embedAT = discord.Embed(title="Edit currently running trivia question"
                                , description="What would you like to edit?"
                                , color=0xFFFFFF)

        await channel.send(embed=embedAT)

    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U0000274C' and payload.user_id in WHITELIST:
        embedAT = discord.Embed(title="Close the currently running trivia question"
                                , description="Are you sure?"
                                , color=0xFFFFFF)

        await channel.send(embed=embedAT)

    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U0001F4C4' and payload.user_id in WHITELIST:
        embedAT = discord.Embed(title="Details about currently running trivia question"
                                , description="Details: your mom"
                                , color=0xFFFFFF)

        await channel.send(embed=embedAT)


# Maybe I can do away with this all together? Slows down the reaction adding by the bot since it /
# triggers this function every time it adds one.
@client.event
async def on_reaction_add(reaction, user):
    #print("reaction was added")
    if 'Apple Trivia' in reaction.message.content and reaction.emoji == '\U00002753':
        embedAT = discord.Embed(title="Start a new question", description="What should the new trivia question be?")
        await user.send(embed=embedAT)

client.run(TOKEN)