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

def get_random_emoji(min=1, max=None):
    if max:
        count = randint(min, max)
    else:
        count = min
    return EMOJI[randrange(len(EMOJI))] * count

MESSAGES = {
    'no_activity': "No one's doing anything :cry:",
    'user_not_found': {
        'nice': "Cannot find user \"{}\"",
        'mean': f"who tf is \"{{}}\" {get_random_emoji()}"
    },
    "user_is_bot": {
        'nice': "**{}** is a bot :robot:",
        'mean': f"**{{}}** is a bot u dummy {get_random_emoji()}"
    },
    'user_is_me': "ya mum lol",
    'user_is_offline': {
        'nice': "**{}** is offline :sleeping:",
        'mean': f"**{{}}** is offline... touching grass maybe... you should try it sometime..... {get_random_emoji()}"
    },
    'caller_is_offline': "you're \"offline\"? :face_with_raised_eyebrow: liar lmao :lying_face:",
    'user_no_activity': {
        'nice': "{} isn't doing anything :smile:",
        'mean': f"{{}} isn't doing anything... go outside {get_random_emoji(1, 3)}"
    },
    'summary_title': "Current Activity in #{}",
    'easter_egg': "merry christmas! :snowman2:"
}

def get_message(key, nice=None, *args):
    arguments = ', '.join(args)
    try:
        if nice is None:
            return MESSAGES[key].format(arguments)
        else:
            if nice is False:
                return MESSAGES[key]["mean"].format(arguments)
            return MESSAGES[key]["nice"].format(arguments)
    except KeyError as e:
        print(e)
        

TYPES = {
    discord.ActivityType.playing: "playing",
    discord.ActivityType.streaming: "streaming",
    discord.ActivityType.listening: "listening to",
    discord.ActivityType.watching: "watching",
    discord.ActivityType.competing: "competing in",
}

PUNCTUATION = ["!", "?", ".", "¿"]

COMMENT = ["cringe", "lol", "lmao", "ok"]

MEAN_BINZ = [
    "not you actually listening to this :joy_cat:",
    "this isn't even music :scream_cat:",
    "cringe :pouting_cat:",
    "shut up :pouting_cat:",
    "ain't no way :skull:"
]

NICE_FLAGS = [
    "be nice"
]

TRUCKS = [":truck:", ":articulated_lorry:", ":pickup_truck:", ":fire_engine:"]

async def send_simple_embed(channel, text):
    await channel.send(embed=discord.Embed(description=text))

def get_time_str(activity):
    if hasattr(activity, 'start'):
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

def rudeify(message, quip=None, force_min1=0, force_max1=4, force_min2=0, force_max2=4):
    rude_msg = message
    rude_msg += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(
        force_min1, force_max1
    )
    if quip:
        rude_msg += " " + quip
        rude_msg += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(
            force_min2, force_max2
        )

    return rude_msg
