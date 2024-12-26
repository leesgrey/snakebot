from discord.ext import commands
from discord import Interaction, app_commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="sync", description="sync slash commands")
    async def sync_tree(self, interaction: Interaction):
        try:
            await interaction.response.defer(thinking=True)
            await self.bot.tree.sync()
            await interaction.followup.send("synced slash commands")

        except Exception as e:
            print(e)

    footer_commands = app_commands.Group(name="footer", description="huh")

    @app_commands.checks.has_permissions(administrator=True)
    @footer_commands.command(
        name="set", description="update footer text for large messages"
    )
    async def set_footer(self, interaction: Interaction, message: str = None):
        try:
            await interaction.response.defer(thinking=True)
            self.bot.footer = message
            if message == None:
                await interaction.followup.send(f"cleared footer text")
            else:
                await interaction.followup.send(f'set footer text to "{message}"')
        except Exception as e:
            print(e)

    @app_commands.checks.has_permissions(administrator=True)
    @footer_commands.command(
        name="clear", description="clear footer text for large messages"
    )
    async def clear_footer(self, interaction: Interaction):
        try:
            # TODO: invoke set_footer()
            await interaction.response.defer(thinking=True)
            self.bot.footer = None
            await interaction.followup.send(f"cleared footer text")
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
