import discord
from discord.ext import commands
import os
import json
import math
from collections import defaultdict
import re
import inflect
from helpers import *

p = inflect.engine()

with open("config.json") as file:
    config = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="wyd ", intents=intents)

@bot.event
async def on_ready():
    print(f"hai im {bot.user}!\n-----------")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="always...")
    )

@bot.command(aliases=["y'all", "yall"])
async def all(ctx):
    mean = True
    channel_activities = defaultdict(list)
    channel_artists = defaultdict(list)
    # this is stinky
    for member in list(filter(lambda member: not member.bot, ctx.channel.members)):
        for activity in member.activities:
            if activity.type == discord.ActivityType.listening:
                channel_artists[activity.artists[0]].append((member.display_name, activity.title))
            elif activity.type != discord.ActivityType.custom:  # used to display status
                if activity.type == discord.ActivityType.playing:
                    details = None
                else:
                    details = activity.details
                if activity.start:
                    hours, minutes = get_time(activity.start)
                    if hours:
                        time_str = f"({hours}{p.plural('hr', hours)} {minutes}{p.plural('min', minutes)})"
                    else:
                        time_str = f"({minutes}{p.plural('min', minutes)})"
                channel_activities[activity.name].append((member.display_name, time_str, details))

    if len(channel_activities) == 0 and len(channel_artists) == 0:
        await ctx.channel.send(embed=discord.Embed(description="no one's doing anything :sob:"))
        return

    test = discord.Embed()
    for artist in channel_artists:
        listener_str = ""
        for listener in channel_artists[artist]:
            listener_str += f"**{listener[0]}**: {listener[1]}\n"
        test.add_field(
            name=format_item(
                artist,
                channel_artists[artist],
                "listening to",
                ":musical_note:",
                mean),
            value=listener_str,
            inline=False)

    for activity in channel_activities:
        gamer_str = ""
        for gamer in channel_activities[activity]:
            gamer_str += f"**{gamer[0]}** {gamer[1]}"
            if gamer[2]:
                gamer_str += f"- *{gamer[2]}*"
            gamer_str += '\n'
        test.add_field(
            name=format_item(
                activity,
                channel_activities[activity],
                "playing",
                ":video_game:",
                mean),
            value=gamer_str,
            inline=False)

    await ctx.channel.send(embed=test)

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#
#    if message.author.id == 928689654818021426:
#        past_two = await message.channel.history(limit = 2).flatten()
#        to_me = past_two[-1].author == bot.user
#        if to_me:
#            if message.content in MEAN_BINZ:
#                await message.add_reaction("\N{CRYING FACE}")
#            else:
#                await message.add_reaction("\N{GRINNING FACE WITH SMILING EYES}")
#        elif message.content in MEAN_BINZ:
#            await message.add_reaction("\N{WHITE UP POINTING INDEX}")
#            if randrange(2) == 0:
#                await message.channel.send("so true binz")
#
#    mean = True 
#    if message.content.lower().startswith("wyd"):
#        message.content = message.content[4:]
#        for flag in NICE_FLAGS:
#            if flag in message.content:
#                message.content = message.content.rsplit(flag, 1)[0].strip()
#                mean = False
#                break
#        
#        if len(message.mentions) > 0:
#            victim = message.mentions[0]
#            
#        elif message.content:
#            victim = message.guild.get_member_named(message.content)
#            if victim is None:
#                if mean:
#                    await message.channel.send(f"who tf is {message.content} {EMOJI[randrange(len(EMOJI))]}")
#                else:
#                    await message.channel.send(f"cannot find user {message.content}")
#                return
#
#        else:
#            victim = message.author
#
#        if victim == bot.user:
#            await message.channel.send("ya mum lol")
#            return
#
#        subject = f"**{victim.display_name}**"
#
#        if victim.bot == True:
#            is_bot = f"{subject} is a bot"
#            if mean:
#                await message.channel.send(rudeify(is_bot, "u dummy", 0, 1, 0, 5))
#            else:
#                await message.channel.send(f"{is_bot} :robot:")
#            return
#
#        if victim.status == discord.Status.offline:
#            offline_msg = f"{subject} is offline"
#            if mean:
#                if victim == message.author:
#                    await message.channel.send(
#                        f"you're \"offline\"? :face_with_raised_eyebrow: liar lmao :lying_face:"
#                    )
#                else:
#                    await message.channel.send(
#                        rudeify(
#                            offline_msg,
#                            "touching grass maybe.... you should try it sometime...........",
#                            3,
#                            6,
#                            0,
#                            1,
#                        )
#                    )
#            else:
#                await message.channel.send(f"{offline_msg} :sleeping:")
#            return
#
#        activities = list(
#            filter(
#                lambda activity: type(activity).__name__ in ["Activity", "Spotify", "Game", "Streaming"],
#                victim.activities
#            )
#        )
#        if activities:
#            activities_msg = f"{subject} {format_activity(activities[0], mean)}"
#            for activity in activities[1:]:
#                activities_msg += f"\nand {format_activity(activity, mean)}"
#            await message.channel.send(activities_msg)
#        else:
#            no_activity = f"{subject} isn't doing anything"
#            if mean:
#                await message.channel.send(rudeify(no_activity, "go outside", 2))
#            else:
#                await message.channel.send(f"{no_activity} :smile:")
#    elif bot.user.mentioned_in(message):
#        if 'help' in message.content:
#            await message.channel.send("```Commands:\nwyd @user: posts @user's current activity, defaults to caller if no user specified\nwyd all: posts the entire channel's current activity\n[command] be nice: forces shamebot to be nice (once) for the specified command```")
#        await message.add_reaction("\N{FACE WITH ONE EYEBROW RAISED}")
#
#
#
#def rudeify(message, quip=None, force_min1=0, force_max1=4, force_min2=0, force_max2=4):
#    rude_msg = message
#    rude_msg += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(
#        force_min1, force_max1
#    )
#    if quip:
#        rude_msg += " " + quip
#        rude_msg += PUNCTUATION[randrange(len(PUNCTUATION))] * randrange(
#            force_min2, force_max2
#        )
#
#    return rude_msg
#
#def format_activity(activity, mean=True):
#    message = ""
#    if type(activity).__name__ == "Spotify":
#        message += f"is listening to **{activity.title}** by **{activity.artists[0]}**"
#    else:
#        message += f"has been {TYPES[activity.type]} **{activity.name}**"
#        hours, minutes = 0, 0
#        if activity.start:
#            hours, minutes = get_time(activity.start)
#        if hours > 1:
#            message += f" for over {hours} hours"
#        elif hours == 1:
#            message += f" for over an hour"
#        else:
#            if minutes == 1:
#                message += " for 1 minute"
#            elif minutes > 1:
#                message += f" for {minutes} minutes"
#            else:
#                message = "is" + message[8:]
#        if hasattr(activity, 'details') and activity.details:
#            message += f" - *{activity.details}*"
#
#    if hasattr(activity, 'name') and len(re.findall(r"\btruck", activity.name.lower())) > 0:
#        message += " let's g" + ("o" * randrange(3, 11)) + " "
#        for truck_idx in range(randrange(3, 8)):
#            message += TRUCKS[randrange(len(TRUCKS))] * randrange(1, 6)
#        message += ":bangbang:"
#    elif mean:
#        message = rudeify(message, COMMENT[randrange(len(COMMENT))])
#
#    return message
#    bot.process_commands(message)

bot.run(config["TOKEN"])
