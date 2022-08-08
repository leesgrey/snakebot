import discord
import os
import datetime
import json
import math
from random import randrange
import re

with open("config.json") as file:
    config = json.load(file)

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

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"hai im {client.user}")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="always...")
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == 928689654818021426:
        past_two = await message.channel.history(limit = 2).flatten()
        to_me = past_two[-1].author == client.user
        if to_me:
            if message.content in MEAN_BINZ:
                await message.add_reaction("\N{CRYING FACE}")
            else:
                await message.add_reaction("\N{GRINNING FACE WITH SMILING EYES}")
        elif message.content in MEAN_BINZ:
            await message.add_reaction("\N{WHITE UP POINTING INDEX}")
            if randrange(2) == 0:
                await message.channel.send("so true binz")

    mean = True 
    if message.content.lower().startswith("wyd"):
        message.content = message.content[4:]
        for flag in NICE_FLAGS:
            if flag in message.content:
                message.content = message.content.rsplit(flag, 1)[0].strip()
                mean = False
                break
        
        if message.content.startswith("all") or message.content.startswith("yall") or message.content.startswith("y\'all"):
            channel_activities = {}
            channel_artists = {}
            for member in list(
                filter(lambda member: not member.bot, message.channel.members)
            ):
                for activity in member.activities:
                    if type(activity).__name__ == "Spotify":
                        artist = activity.artists[0]
                        new_listener = (member.display_name, activity.title)
                        if artist in channel_artists:
                            channel_artists[artist].append(new_listener)
                        else:
                            channel_artists[artist] = [new_listener]
                    elif type(activity).__name__ in ["Activity", "Game", "Streaming"]:
                        time_str = " "
                        if activity.start:
                            time_str += "("
                            hours, minutes = get_time(activity.start)
                            if hours == 1:
                                time_str += "1 hr "
                            elif hours > 1:
                                time_str += f"{hours} hrs "
                            time_str += f"{minutes} min"
                            time_str += ")"
                        details = None
                        if type(activity).__name__ == "Activity":
                            details = activity.details
                        new_gamer = (member.display_name, time_str, details)
                        if activity.name in channel_activities:
                            channel_activities[activity.name].append(new_gamer)
                        else:
                            channel_activities[activity.name] = [new_gamer]

            if len(channel_activities) == 0 and len(channel_artists) == 0:
                await message.channel.send("no one's doing anything :sob:")
                return

            music_str = ""
            for artist in channel_artists:
                music_str += format_item(
                    artist,
                    channel_artists[artist],
                    "listening to",
                    ":musical_note:",
                    mean,
                )
                for listener in channel_artists[artist]:
                    music_str += f"> **{listener[0]}**: {listener[1]}\n"

            activity_str = ""
            for activity in channel_activities:
                activity_str += format_item(
                    activity,
                    channel_activities[activity],
                    "playing",
                    ":video_game:",
                    mean,
                )
                for gamer in channel_activities[activity]:
                    activity_str += f"> **{gamer[0]}**{gamer[1]}"
                    if gamer[2]:
                        activity_str += f"- *{gamer[2]}*"
                    activity_str += '\n'

            await message.channel.send(f"{activity_str}{music_str}")
            return

        if len(message.mentions) > 0:
            victim = message.mentions[0]
            
        elif message.content:
            victim = message.guild.get_member_named(message.content)
            if victim is None:
                if mean:
                    await message.channel.send(f"who tf is {message.content} {EMOJI[randrange(len(EMOJI))]}")
                else:
                    await message.channel.send(f"cannot find user {message.content}")
                return

        else:
            victim = message.author

        if victim == client.user:
            await message.channel.send("ya mum lol")
            return

        subject = f"**{victim.display_name}**"

        if victim.bot == True:
            is_bot = f"{subject} is a bot"
            if mean:
                await message.channel.send(rudeify(is_bot, "u dummy", 0, 1, 0, 5))
            else:
                await message.channel.send(f"{is_bot} :robot:")
            return

        if victim.status == discord.Status.offline:
            offline_msg = f"{subject} is offline"
            if mean:
                if victim == message.author:
                    await message.channel.send(
                        f"you're \"offline\"? :face_with_raised_eyebrow: liar lmao :lying_face:"
                    )
                else:
                    await message.channel.send(
                        rudeify(
                            offline_msg,
                            "touching grass maybe.... you should try it sometime...........",
                            3,
                            6,
                            0,
                            1,
                        )
                    )
            else:
                await message.channel.send(f"{offline_msg} :sleeping:")
            return

        activities = list(
            filter(
                lambda activity: type(activity).__name__ in ["Activity", "Spotify", "Game", "Streaming"],
                victim.activities
            )
        )
        if activities:
            activities_msg = f"{subject} {format_activity(activities[0], mean)}"
            for activity in activities[1:]:
                activities_msg += f"\nand {format_activity(activity, mean)}"
            await message.channel.send(activities_msg)
        else:
            no_activity = f"{subject} isn't doing anything"
            if mean:
                await message.channel.send(rudeify(no_activity, "go outside", 2))
            else:
                await message.channel.send(f"{no_activity} :smile:")
    elif client.user.mentioned_in(message):
        if 'help' in message.content:
            await message.channel.send("```Commands:\nwyd @user: posts @user's current activity, defaults to caller if no user specified\nwyd all: posts the entire channel's current activity\n[command] be nice: forces shamebot to be nice (once) for the specified command```")
        await message.add_reaction("\N{FACE WITH ONE EYEBROW RAISED}")


def get_time(start):
    seconds = (datetime.datetime.utcnow() - start).seconds
    hours, seconds = divmod(seconds, 3600)
    minutes = seconds // 60
    return (hours, minutes)

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


def format_activity(activity, mean=True):
    message = ""
    if type(activity).__name__ == "Spotify":
        message += f"is listening to **{activity.title}** by **{activity.artists[0]}**"
    else:
        message += f"has been {TYPES[activity.type]} **{activity.name}**"
        hours, minutes = 0, 0
        if activity.start:
            hours, minutes = get_time(activity.start)
        if hours > 1:
            message += f" for over {hours} hours"
        elif hours == 1:
            message += f" for over an hour"
        else:
            if minutes == 1:
                message += " for 1 minute"
            elif minutes > 1:
                message += f" for {minutes} minutes"
            else:
                message = "is" + message[8:]
        if hasattr(activity, 'details') and activity.details:
            message += f" - *{activity.details}*"

    if hasattr(activity, 'name') and len(re.findall(r"\btruck", activity.name.lower())) > 0:
        message += " let's g" + ("o" * randrange(3, 11)) + " "
        for truck_idx in range(randrange(3, 8)):
            message += TRUCKS[randrange(len(TRUCKS))] * randrange(1, 6)
        message += ":bangbang:"
    elif mean:
        message = rudeify(message, COMMENT[randrange(len(COMMENT))])

    return message


client.run(config["TOKEN"])
