import asyncio

import discord
import requests
from discord.ext import tasks, commands
import time


# Class for holding information on a trivia question
class TriviaQuestion:
    #question = None
    #answers = []
    #end_time = None

    def __init__(self):
        self.question = None
        self.answers = []
        self.end_time = None

    def changeQuestion(self, question):
        self.question = question

    def changeAnswers(self, answers):
        self.answers = answers

    def changeEndTime(self, end_time):
        self.end_time = end_time

    def resetTrivia(self):
        self.question = None
        self.answers = []
        self.end_time = None


# Token for client login
TOKEN = ''
THREADS = []
QUESTION = TriviaQuestion()
WHITELIST = []
client = discord.Client()


# Helper function for white list checking
def whiteListCheck(message):
    return message.author.id in WHITELIST


# Main 'Apple Trivia' driver
async def appleTrivia(authr):
    # Embed message with all of the options
    embed_at = discord.Embed(title="Apple Trivia", description="Hello! What do you want to do?", color=0xFFFFFF)
    embed_at.add_field(name="\U00002753 option"
                       , value="Start a new trivia question"
                       , inline=False)

    embed_at.add_field(name="\U0000270F option"
                       , value="Edit the currently running trivia question"
                       , inline=False)

    embed_at.add_field(name="\U0000274C option"
                       , value="Close the currently running trivia question"
                       , inline=False)

    embed_at.add_field(name="\U0001F4C4 option"
                       , value="View details about the currently running trivia question"
                       , inline=False)

    # Send message to user
    msg = await authr.send(embed=embed_at)

    # Add reactions as the option buttons
    await msg.add_reaction('\U00002753')
    await msg.add_reaction('\U0000270F')
    await msg.add_reaction('\U0000274C')
    await msg.add_reaction('\U0001F4C4')


# New Question Option
async def newQuestion(chnl):
    embed_at = discord.Embed(title="Start a new question"
                             , description="What should the new trivia question be?"
                             , color=0xFFFFFF)

    await chnl.send(embed=embed_at)
    question = await client.wait_for('message', check=whiteListCheck)
    print(question.content)
    QUESTION.changeQuestion(question.content)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('$help'))


# Might not need the thread here since the bot is now dedicated to Apple Trivia.
# Though might need to make a thread for a trivia question.
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

        elif "Class check" in message.content:
            print(QUESTION.question)


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

    # New Question
    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U00002753' and payload.user_id in WHITELIST:
        await newQuestion(channel)

    # Edit Question
    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U0000270F' and payload.user_id in WHITELIST:
        embed_at = discord.Embed(title="Edit currently running trivia question"
                                , description="What would you like to edit?"
                                , color=0xFFFFFF)

        await channel.send(embed=embed_at)

    # Close Question
    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U0000274C' and payload.user_id in WHITELIST:
        embed_at = discord.Embed(title="Close the currently running trivia question"
                                , description="Are you sure?"
                                , color=0xFFFFFF)

        await channel.send(embed=embed_at)

    # Details of Question
    if 'Apple Trivia' in embed.title and payload.emoji.name == '\U0001F4C4' and payload.user_id in WHITELIST:
        embed_at = discord.Embed(title="Details about currently running trivia question"
                                , description="Details: your mom"
                                , color=0xFFFFFF)

        await channel.send(embed=embed_at)


# Maybe I can do away with this all together? Slows down the reaction adding by the bot since it /
# triggers this function every time it adds one.
#@client.event
#async def on_reaction_add(reaction, user):
#    #print("reaction was added")
#    if 'Apple Trivia' in reaction.message.content and reaction.emoji == '\U00002753':
#        embed_at = discord.Embed(title="Start a new question", description="What should the new trivia question be?")
#        await user.send(embed=embed_at)

client.run(TOKEN)