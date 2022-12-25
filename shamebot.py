import discord
from discord.ext import commands
import json
import asyncio
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prefix")
args = parser.parse_args()

with open("config.json") as file:
    config = json.load(file)

if args.prefix:
    bot = commands.Bot(command_prefix=args.prefix, intents=discord.Intents.all())
else:
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

async def load_extensions():
    for cog_file in ["ActivityCommands"]:
        try:
            await bot.load_extension(f"cogs.{cog_file}")
            print(f"Loaded extension {cog_file}")
        except (commands.ExtensionNotFound, commands.ExtensionAlreadyLoaded, commands.NoEntryPointError, commands.ExtensionFailed) as e:
            print(f"Could not load extension - {e}")

@bot.event
async def on_ready():
    print(f"hai im {bot.user} (prefix: {bot.command_prefix})")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="always...")
    )

async def main():
    await load_extensions()
    async with bot:
        await bot.start(config["TOKEN"])

asyncio.run(main())
