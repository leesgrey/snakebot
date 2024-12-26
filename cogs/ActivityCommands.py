from discord.ext import commands
from helpers import *
from datetime import datetime
from classes import (
    ArtistActivity,
    Listener,
    GameActivity,
    Gamer,
    StreamActivity,
    Streamer,
)
import re
from random import randrange, random
from discord import Interaction, app_commands, Member


class ActivityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.footer = None

    # Print user or channel activity
    @app_commands.command(
        name="wyd",
        description="send current user (or channel, if unspecified) activity",
    )
    async def wyd(self, interaction: Interaction, target: Member = None):
        await interaction.response.defer(thinking=True)
        if target is None:
            try:
                await interaction.followup.send(
                    embed=self.get_channel_embed(
                        interaction.channel.members,
                        get_message("summary_title", interaction.channel.name),
                    )
                )
            except Exception as e:
                print(f"Could not send channel activity - {e}")
        else:
            try:
                await self.send_user_activity(interaction, target.id)
            except Exception as e:
                print(f"Could not send user activity - {e}")

    def get_channel_activities(self, members):
        activities = {}

        for member in members:
            if member.bot:
                continue

            for activity in member.activities:
                if activity.type == discord.ActivityType.listening:
                    if "listening" not in activities:
                        activities["listening"] = {}
                    artist = activity.artists[0]
                    if artist not in activities["listening"]:
                        activities["listening"][artist] = ArtistActivity(artist)
                    activities["listening"][artist].add_user(
                        member.display_name, activity.title  # song title
                    )
                elif activity.type == discord.ActivityType.streaming:
                    if "streaming" not in activities:
                        activities["streaming"] = {}
                    game = activity.game
                    if game not in activities["streaming"]:
                        activities["streaming"][game] = StreamActivity(game)
                    activities["streaming"][game].add_user(
                        member.display_name,
                        activity.url,  # stream link
                        activity.platform,  # stream platform
                        activity.name,  # stream title
                    )
                elif activity.type == discord.ActivityType.playing:
                    if "" not in activities:
                        activities["playing"] = {}
                    game = activity.name
                    if game not in activities["playing"]:
                        activities["playing"][game] = GameActivity(game)
                    activities["playing"][game].add_user(
                        member.display_name,
                        get_time_str(activity),
                        getattr(activity, "details", None),
                    )
                """
                match activity.type:
                    case discord.ActivityType.listening:
                        if "listening" not in activities:
                            activities["listening"] = {}
                        artist = activity.artists[0]
                        if artist not in activities["listening"]:
                            activities["listening"][artist] = ArtistActivity(artist)
                        activities["listening"][artist].add_user(
                            member.display_name, activity.title  # song title
                        )
                    case discord.ActivityType.streaming:
                        if "streaming" not in activities:
                            activities["streaming"] = {}
                        game = activity.game
                        if game not in activities["streaming"]:
                            activities["streaming"][game] = StreamActivity(game)
                        activities["streaming"][game].add_user(
                            member.display_name,
                            activity.url,  # stream link
                            activity.platform,  # stream platform
                            activity.name,  # stream title
                        )
                    case discord.ActivityType.playing:
                        if "" not in activities:
                            activities["playing"] = {}
                        game = activity.name
                        if game not in activities["playing"]:
                            activities["playing"][game] = GameActivity(game)
                        activities["playing"][game].add_user(
                            member.display_name,
                            get_time_str(activity),
                            getattr(activity, "details", None),
                        )
                """
        return activities

    def get_channel_embed(self, members, title=None):
        activities = self.get_channel_activities(members)

        activity_fields = []
        for activity_type in activities:
            for activity in activities[activity_type]:
                activity_fields.append(activities[activity_type][activity].get_field())

        summary_embed = discord.Embed.from_dict(
            {
                "title": title,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "description": (
                    None if len(activity_fields) > 0 else get_message("no_activity")
                ),
                "fields": activity_fields,
            }
        )
        summary_embed.set_footer(text=self.bot.footer)
        return summary_embed

    async def send_user_activity(self, interaction, target_id):
        target = interaction.guild.get_member(target_id)
        if target.bot:
            if target == self.bot.user:
                await interaction.followup.send(get_message("user_is_me"))
                return
            await send_simple_embed(
                interaction.followup, get_message("user_is_bot", target.display_name)
            )
            return

        if target.status == discord.Status.offline:
            await send_simple_embed(
                interaction.followup,
                get_message("user_is_offline", target.display_name),
            )
            return

        activities = list(
            filter(
                lambda activity: activity.type != discord.ActivityType.custom,
                target.activities,
            )
        )
        if activities:
            await interaction.followup.send(
                embed=self.get_user_embed(activities, target)
            )
        else:
            await send_simple_embed(
                interaction.followup,
                get_message("user_no_activity", target.display_name),
            )

    def get_user_activity_field(self, activity):
        if activity.type == discord.ActivityType.listening:
            return {
                "name": Listener.format_user_str(activity.title, activity.artists[0]),
                "value": Listener.format_user_details(
                    activity.duration, activity.start, activity.track_url
                ),
            }
        elif activity.type == discord.ActivityType.streaming:
            return {
                "name": Streamer.format_user_str(activity.game, activity.platform),
                "value": Streamer.format_stream_details(activity.url, activity.name),
            }
        else:
            return {
                "name": Gamer.format_user_str(activity.name),
                "value": Gamer.format_user_details(
                    get_time_str(activity), getattr(activity, "details", None)
                ),
            }

    def get_user_embed(self, activities, user):
        activity_fields = []
        thumbnail = None
        for activity in activities:
            activity_fields.append(self.get_user_activity_field(activity))
            if hasattr(activity, "album_cover_url"):
                thumbnail = activity.album_cover_url

        if random() < 0.1:
            activity_fields.append(
                list(FUN_USER_FIELDS.values())[randrange(len(FUN_USER_FIELDS))]
            )

        user_embed = discord.Embed.from_dict(
            {
                "fields": activity_fields,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        user_embed.set_author(
            name=f"{user.display_name}'s current activity", icon_url=user.avatar
        )
        user_embed.set_footer(text=self.bot.footer)
        if thumbnail:
            user_embed.set_thumbnail(url=thumbnail)
        return user_embed


async def setup(bot):
    await bot.add_cog(ActivityCommands(bot))
