from discord.ext import commands
from helpers import *
from PIL import Image
from io import BytesIO
import re
import discord
from discord import Interaction, app_commands


class SaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="hoohoohee")
    async def say(self, interaction: Interaction):
        try:
            await self.said.callback(self, interaction)
        except Exception as e:
            print(e)

    @app_commands.command(name="said", description="heeheehoo")
    async def said(self, interaction: Interaction, target: str = None):
        try:
            await interaction.response.defer(thinking=True)
            if target is None:
                speaker = interaction.user
            else:
                id_match = re.match(r"<@!?([0-9]{17,19})>$", target)
                if id_match is not None:
                    speaker = interaction.guild.get_member(int(id_match.group(1)))
                else:
                    speaker = interaction.guild.get_member_named(target)

            if speaker is None:
                await interaction.followup.send(f"{target} not found")
                return

            speaker_bytes = await self.get_avatar(speaker)

            # ??
            final_buffer = await self.bot.loop.run_in_executor(
                None, self.create_speech_img, speaker_bytes
            )

            # read docs...
            file = discord.File(filename="speech.png", fp=final_buffer)

            await interaction.followup.send(file=file)
        except Exception as e:
            print(e)

    @staticmethod
    async def get_avatar(user):
        return await user.display_avatar.replace(format="png", size=512).read()

    def get_emoji():
        pass

    @staticmethod
    def create_speech_img(speaker):
        bubble_img = Image.open("assets/bubbleimg.png")
        bubble_mask = Image.open("assets/bubblemask.png")

        with Image.open(BytesIO(speaker)) as speaker_img:
            speaker_img = speaker_img.resize((256, 256))
            speaker_img.paste(bubble_img, mask=bubble_mask)

            final_buffer = BytesIO()
            speaker_img.save(final_buffer, "png")

        bubble_img.close()
        bubble_mask.close()

        final_buffer.seek(0)
        return final_buffer


async def setup(bot):
    await bot.add_cog(SaidCommands(bot))
