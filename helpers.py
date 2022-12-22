import discord
from datetime import datetime, timezone
from random import randrange

TYPES = {
    discord.ActivityType.playing: "playing",
    discord.ActivityType.streaming: "streaming",
    discord.ActivityType.listening: "listening to",
    discord.ActivityType.watching: "watching",
    discord.ActivityType.competing: "competing in",
}

PUNCTUATION = ["!", "?", ".", "¿"]

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
    message += ":\n"

    return message