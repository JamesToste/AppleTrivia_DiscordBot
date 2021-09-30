import asyncio

import discord
import requests
from discord.ext import tasks, commands
import time

# Token for client login
TOKEN = ''
THREADS = []
WHITELIST = [203210022644219904, 197636877845528576]
client = discord.Client()


# Main 'Apple Trivia' driver
async def appleTrivia(authr):
    """
    counter = 0
    await authr.send("Hello, Christian. What should the question for Apple Trivia be?")
    question = await client.wait_for('message', check=lambda message: message.author != client.user)
    await auth.send(question.content)
    while counter < 5:
        counter += 1
        #print(time.clock_gettime(time.CLOCK_BOOTTIME))
        await auth.send("Await " + str(counter))
        await asyncio.sleep(2)
    await auth.send("Done waiting")
    """
    # Embed message with all of the options
    embedAT = discord.Embed(title="Apple Trivia", description="Hello Christian, what do you want to do?")
    embedAT.add_field(name="\U00002753 option", value="Start a new trivia question", inline=False)
    #embedAT.add_field(name="field1", value="hi", inline=False)
    #embedAT.add_field(name="field1", value="hi", inline=False)
    #embedAT.add_field(name="field1", value="hi", inline=False)

    msg = await authr.send(embed=embedAT)

    await msg.add_reaction('\U00002753')


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
        else:
            print(message.author)
            await message.author.send("Unauthorized attempted access. Your Discord name has been recorded!")


@client.event
async def on_reaction_add(reaction, user):
    # GOTTA FINISH THIS UP. HOW TO READ EMBED CONTENT?
    if 'Apple Trivia' in reaction.message.content and reaction.emoji == '\U00002753':
        embedAT = discord.Embed(title="Start a new question", description="What should the new trivia question be?")
        await user.send(embed=embedAT)

client.run(TOKEN)