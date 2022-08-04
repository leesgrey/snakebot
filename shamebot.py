import discord
import os
import datetime
from random import randrange
import json

with open('config.json') as file:
  config = json.load(file)

TYPES = {
  discord.ActivityType.playing: 'playing',
  discord.ActivityType.streaming: 'streaming',
  discord.ActivityType.listening: 'listening to',
  discord.ActivityType.watching: 'watching',
  discord.ActivityType.competing: 'competing in'
}

PUNCTUATION = [
  '!',
  '?',
  '.'
]

EMOJI = [
  ':sob:',
  ':skull:',
  ':joy:'
]

COMMENT = [
  'cringe',
  'lol',
  'lmao',
  'ok'
]

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'hai im {client.user}')

@client.event
async def on_message(message):
  if message.content.startswith('//wyd'):
    if len(message.mentions) > 0:
      victim = message.mentions[0]
      if victim == client.user:
        await message.channel.send('ya mum lol')
        return

      target = f'{victim.display_name} is'
      activities = list(filter(lambda activity: type(activity).__name__ in ['Activity', 'Spotify'], victim.activities))
    else:
      target = 'ur'
      activities = list(filter(lambda activity: type(activity).__name__ in ['Activity', 'Spotify'], message.author.activities))
    if activities:
      await message.channel.send(f'{target} {format_activity(activities[0])}')
      for activity in activities[1:]:
        await message.channel.send(f'and {format_activity(activity)}')
    else:
      await message.channel.send(f'{target} not doing anything :/ go outside...')

def format_activity(activity):
  message = ''
  if type(activity).__name__ == 'Spotify':
    message += f'listening to {activity.title} by {activity.artist}'
  else:
    message += f'{TYPES[activity.type]} {activity.name}'
    hours = (datetime.datetime.now() - datetime.datetime.fromtimestamp(activity.timestamps['start'] // 1000)).seconds // 3600
    if hours == 1:
      message += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(4)
      message += f' for over an hour'
    elif hours > 1:
      message += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(4)
      message += f' for over {hours} hours'

  message += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(4)
  message += ' ' + COMMENT[randrange(len(COMMENT))]
  message += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(4)
  
  return message

client.run(config['TOKEN'])