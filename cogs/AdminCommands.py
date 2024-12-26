from discord.ext import commands
from discord import app_commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="sync", description="wooah")
    async def sync_tree(self):
        await self.bot.tree.sync()


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
