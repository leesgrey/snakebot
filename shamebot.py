import discord
import os
import datetime
import json
import math
from random import randrange

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
  ':joy:',
  ':face_with_raised_eyebrow:'
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
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='always...'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  mean = True
  if 'be nice' in message.content:
    mean = False

  if message.content.startswith('wyd'):
    if message.content.startswith('all', 4):
      channel_activities = {}
      channel_artists= {}
      for member in list(filter(lambda member: not member.bot, message.channel.members)):
        for activity in member.activities:
          if type(activity).__name__ == 'Spotify':
            artist = activity.artists[0]
            new_listener = (member.display_name, activity.title)
            if artist in channel_artists:
              channel_artists[artist].append(new_listener)
            else:
              channel_artists[artist] = [new_listener]
          elif type(activity).__name__ == 'Activity':
            time_str = ''
            if 'start' in activity.timestamps:
              time_str += '('
              hours, minutes = get_time(activity.timestamps['start'])
              if hours == 1:
                time_str += '1 hr '
              elif hours > 1:
                time_str += f'{hours} hr '
              time_str += f'{minutes} minutes'
              time_str += ')'
            new_gamer = (member.display_name, time_str)
            if activity.name in channel_activities:
              channel_activities[activity.name].append(new_gamer)
            else:
              channel_activities[activity.name] = [new_gamer]
          
      music_str = ''
      for artist in channel_artists:
        music_str += format_item(artist, channel_artists[artist], 'listening to', ':musical_note:', mean)
        for listener in channel_artists[artist]:
          music_str += f'> **{listener[0]}**: {listener[1]}\n'
      
      activity_str = ''
      for activity in channel_activities:
        activity_str += format_item(activity, channel_activities[activity], 'playing', ':video_game:', mean)
        for gamer in channel_activities[activity]:
          activity_str += f'> **{gamer[0]}** {gamer[1]}\n'

      await message.channel.send(f'{activity_str}\n{music_str}')
      return

    if len(message.mentions) > 0:
      victim = message.mentions[0]
      if victim == client.user:
        await message.channel.send('ya mum lol')
        return

    else:
      victim = message.author
    subject = victim.display_name

    if victim.status == discord.Status.offline:
      offline_msg = f'{subject} is offline'
      if mean:
        if victim == message.author:
          await message.channel.send(f'You\'re offline? :face_with_raised_eyebrow: liar lmao')
        else:
          await message.channel.send(rudeify(offline_msg, 'touching grass maybe.... you should try it sometime', 3, 6))
      else:
        await message.channel.send(f'{offline_msg} :sleeping:')

      return

    activities = list(filter(lambda activity: type(activity).__name__ in ['Activity', 'Spotify'], victim.activities))
    if activities:
      await message.channel.send(f'{subject} {format_activity(activities[0], mean)}')
      for activity in activities[1:]:
        await message.channel.send(f'and {format_activity(activity, mean)}')
    else:
      no_activity = f'{subject} is not doing anything'
      if mean:
        await message.channel.send(rudeify(no_activity, 'go outside', 1))
      else:
        await message.channel.send(f'{no_activity} :smile:')

def get_time(start): # defaults to hours
  seconds = (datetime.datetime.now() - datetime.datetime.fromtimestamp(start // 1000)).seconds
  hours, seconds = divmod(seconds, 3600)
  minutes = seconds // 60
  return (hours, minutes)

def rudeify(message, quip = None, force_min = 0, force_max = 4):
  rude_msg = ''
  rude_msg += message
  rude_msg += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(force_min, force_max)
  if quip:
    rude_msg += ' ' + quip
    rude_msg += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(force_min, force_max)

  return rude_msg

def format_item(name, users, verb, emoji = '', mean = True):
  message = ''
  if emoji:
    message += f'{emoji} '
  if len(users) == 1:
    message += '1 person is'
  else:
    message += f'{len(users)} people are'
  message += f' {verb} **{name}**'
  if mean:
    message += f' {EMOJI[randrange(len(EMOJI))]}'
  message += ':\n'

  return message

def format_activity(activity, mean = True):
  message = ''
  if type(activity).__name__ == 'Spotify':
    message += f'is listening to {activity.title} by {activity.artists[0]}'
  else:
    message += f'has been {TYPES[activity.type]} {activity.name}'
    hours, minutes = 0, 0
    if 'start' in activity.timestamps:
      hours, minutes = get_time(activity.timestamps['start'])
    if hours > 1:
      message += f' for over {hours} hours'
    elif hours > 1:
      message += f' for over an hour'
    else:
      if minutes == 1:
        message += ' for 1 minute'
      elif minutes > 1:
        message += f' for {minutes} minutes'
      else:
        message = 'is' + message[8:]
  
  if mean:
    message = rudeify(message, COMMENT[randrange(len(COMMENT))])
  
  return message

client.run(config['TOKEN'])