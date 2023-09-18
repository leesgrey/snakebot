from discord.ext import commands
from helpers import *
from datetime import datetime
from classes import ArtistActivity, Listener, GameActivity, Gamer, StreamActivity, Streamer
import re
from random import randrange, random
import json

# TODO: move to slash commands
# commands that output user and server activity
class ActivityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.footer = None

        with open("config.json") as file:
            self.config = json.load(file)

    # TODO: move to admin cog
    @commands.command()
    async def set_footer(self, ctx, message=None):
        if ctx.author.id in self.config["ADMIN_IDS"]:
            self.footer = message
            if message == None:
                await ctx.channel.send(f"Cleared footer text")
            else:
                await ctx.channel.send(f"Set footer text to \"{message}\"")
        else:
            await ctx.channel.send("Noooo :pouting_cat:")

    # TODO: move to admin cog
    @commands.command()
    async def clear_footer(self, ctx):
        await self.set_footer(ctx);

    # Print user or channel activity
    @commands.command()
    async def wyd(self, ctx, target=None):
        if target in ["all", "y'all", "yall"]:
            try:
                await self.send_summary(
                    ctx.channel,
                    self.get_summary_activities(ctx.channel.members),
                    get_message('summary_title', ctx.channel.name))
            except Exception as e:
                print(f"Could not send channel activity - {e}")
        else:
            try:
                await self.send_user_activity(ctx, target)
            except Exception as e:
                print(f"Could not send user activity - {e}")

    def get_summary_activities(self, members):
        games = {}
        artists = {}
        streams = {}
        # kinda stinky
        for member in list(filter(lambda member: not member.bot, members)):
            print(member)
            for activity in list(filter(lambda activity: activity.type != discord.ActivityType.custom, member.activities)):
                print(activity)
                if activity.type == discord.ActivityType.listening:
                    if activity.artists[0] not in artists:
                        artists[activity.artists[0]] = ArtistActivity(activity.artists[0])
                    artists[activity.artists[0]].add_user(
                        member.display_name,
                        activity.title)
                elif activity.type == discord.ActivityType.streaming:
                    if activity.game not in streams:
                        streams[activity.game] = StreamActivity(activity.game)
                    streams[activity.game].add_user(
                        member.display_name,
                        activity.url,
                        activity.platform,
                        activity.name)
                elif activity.type == discord.ActivityType.playing:  # custom used to display custom status
                    if activity.name not in games:
                        games[activity.name] = GameActivity(activity.name)
                    games[activity.name].add_user(
                        member.display_name,
                        get_time_str(activity),
                        getattr(activity, 'details', None))
        return [games, artists, streams]

    async def send_summary(self, channel, activities, title=None):
        activity_fields = []
        empty_description = None
        for activity_group in activities:
            for activity in activity_group.values():
                activity_fields.append(activity.get_field())

        if len(activity_fields) == 0:
            empty_description = get_message('no_activity')

        summary_embed = discord.Embed.from_dict({
            'title': title,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'description': empty_description,
            'fields': activity_fields
        })
        summary_embed.set_footer(text=self.footer)
        summary_embed.set_thumbnail(url=channel.guild.icon)
        await channel.send(embed=summary_embed)

    async def send_user_activity(self, ctx, target=None):
        if target is None:
            user = ctx.author
        else:
            id_match = re.match(r"<@!?([0-9]{17,19})>$", target)
            if id_match is not None:
                user = ctx.guild.get_member(int(id_match.group(1)))
            else:
                user = ctx.guild.get_member_named(target)

        if user is None:
            await send_simple_embed(ctx.channel, get_message('user_not_found', target))
            return
        
        if user.bot is True:
            if user == self.bot.user:
                await ctx.channel.send(get_message('user_is_me'))
                return
            await send_simple_embed(ctx.channel, get_message('user_is_bot', user.display_name))
            return

        if user.status == discord.Status.offline:
            await send_simple_embed(ctx.channel, get_message('user_is_offline', user.display_name))
            return

        activities = list(filter(lambda activity: activity.type != discord.ActivityType.custom, user.activities))
        if activities:
            await ctx.channel.send(embed=self.get_user_embed(activities, user))
        else:
            await send_simple_embed(ctx.channel, get_message('user_no_activity', user.display_name))

    def get_user_activity_field(self, activity):
        if activity.type == discord.ActivityType.listening:
            return {
                'name': Listener.format_user_str(activity.title, activity.artists[0]),
                'value': Listener.format_user_details(activity.duration, activity.start, activity.track_url)
                }
        elif activity.type == discord.ActivityType.streaming:
            return {
                'name': Streamer.format_user_str(activity.game, activity.platform),
                'value': Streamer.format_stream_details(activity.url, activity.name)
            }
        else:
            return {
                'name': Gamer.format_user_str(activity.name),
                'value': Gamer.format_user_details(get_time_str(activity), getattr(activity, 'details', None))
            }

    def get_user_embed(self, activities, user):
        activity_fields = []
        thumbnail = None
        for activity in activities:
            activity_fields.append(self.get_user_activity_field(activity))
            if hasattr(activity, "album_cover_url"):
                thumbnail = activity.album_cover_url
        
        if random() < 0.1:
            activity_fields.append(list(FUN_USER_FIELDS.values())[randrange(len(FUN_USER_FIELDS))])

        user_embed = discord.Embed.from_dict({
            'fields': activity_fields,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        })
        user_embed.set_author(name=f"{user.display_name}'s current activity", icon_url=user.avatar)
        user_embed.set_footer(text=self.footer)
        if thumbnail:
            user_embed.set_thumbnail(url=thumbnail)
        return user_embed       


async def setup(bot):
	await bot.add_cog(ActivityCommands(bot))