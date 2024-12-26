import discord
from discord.ext import commands
import json
import asyncio
import argparse

with open("config.json") as file:
    config = json.load(file)

# allow alternate prefix for testing, default to ?
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prefix")
args = parser.parse_args()
if args.prefix:
    bot = commands.Bot(command_prefix=args.prefix, intents=discord.Intents.all())
else:
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())


async def load_extensions():
    for cog_file in ["AdminCommands", "ActivityCommands", "SaidCommands"]:
        try:
            await bot.load_extension(f"cogs.{cog_file}")
            print(f"Loaded extension {cog_file}")
        except (
            commands.ExtensionNotFound,
            commands.ExtensionAlreadyLoaded,
            commands.NoEntryPointError,
            commands.ExtensionFailed,
        ) as e:
            print(f"Could not load extension - {e}")


@bot.event
async def on_ready():
    print(f"{bot.user} online B] (prefix: {bot.command_prefix})")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name="around")
    )


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.add_reaction("\N{WAVING HAND SIGN}")
    await bot.process_commands(message)


async def main():
    await load_extensions()
    async with bot:
        await bot.login(config["TOKEN"])


asyncio.run(main())
