import discord
from datetime import datetime, timezone
from random import randrange, randint
import inflect
p = inflect.engine()

EMOJI = [
    ":sob:",
    ":skull:",
    ":joy:",
    ":face_with_raised_eyebrow:",
    ":flushed:",
    ":scream:",
    ":thinking_face:",
    ":rofl:",
    ":face_with_hand_over_mouth:",
    ":grimacing:",
]

FUN_USER_FIELDS = {
    'worm' : {
        'name': ":worm: playing with they worm",
        'value': "who up?"
    },
    'simp': {
        'name': ":person_bowing: simping",
        'value': "down bad as usual..."
    },
    'orb': {
        'name': ":crystal_ball: pondering they orb",
        'value': ".   +✵    .  ✹  *· .     ✫   · "
    },
    'wonka': {
        'name': ":tophat: wonkin they willy",
        'value': ":flushed: :chocolate_bar:"
    }
}

def get_random_emoji(min=1, max=None):
    if max:
        count = randint(min, max)
    else:
        count = min
    return EMOJI[randrange(len(EMOJI))] * count

MESSAGES = {
    'no_activity': "No one's doing anything :cry:",
    'user_not_found': "Cannot find user \"{}\"",
    "user_is_bot": "**{}** is a bot :robot:",
    'user_is_me': "ya mum lol",
    'user_is_offline': "**{}** is offline :sleeping:",
    'user_no_activity': "**{}** isn't doing anything :person_standing:",
    'summary_title': "Current Activity in #{}",
}

def get_message(key, *args):
    arguments = ', '.join(args)
    try:
        return MESSAGES[key].format(arguments)
    except KeyError as e:
        print("wah " + e)
        
async def send_simple_embed(channel, text):
    await channel.send(embed=discord.Embed(description=text))

def get_time_str(activity):
    if hasattr(activity, 'start') and activity.start is not None:
        hours, minutes = get_time(activity.start)
        if hours:
            return(f"({hours}{p.plural('hr', hours)} {minutes}{p.plural('min', minutes)})")
        else:
            return(f"({minutes}{p.plural('min', minutes)})")

def get_time(start):
    seconds = (datetime.now(timezone.utc) - start).seconds
    hours, seconds = divmod(seconds, 3600)
    minutes = seconds // 60
    return (hours, minutes)

def format_item(name, users, verb, emoji="", mean=True):
    message = ""
    if emoji:
        message += f"{emoji} "
    if len(users) == 1:
        message += "1 person is"
    else:
        message += f"{len(users)} people are"
    message += f" {verb} **{name}**"
    if mean:
        message += f" {EMOJI[randrange(len(EMOJI))]}"
    message += "\n"

    return message
