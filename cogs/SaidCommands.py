from discord.ext import commands
from helpers import *
from PIL import Image

# TODO: move to slash commands
# commands that output user and server activity
class SaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['say', 'says'])
    async def said(self, ctx, target=None):
        bytes = await ctx.author.display_avatar.with_size(128).read()

async def setup(bot):
	await bot.add_cog(SaidCommands(bot))