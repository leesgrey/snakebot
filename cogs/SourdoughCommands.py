from discord.ext import commands
from discord import Interaction, app_commands
import math


class SourdoughCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sourdough", description="get how many feedings you need to reach a target amount of starter")
    @app_commands.describe(current="how much starter do you have?")
    @app_commands.describe(target="how much starter do you need?")
    @app_commands.describe(leftover="how much starter do you want left over?")
    @app_commands.describe(ratio="if not 1:1:1, what ratio of starter:flour:water do you use for feeding?")
    @app_commands.describe(verbose="show your work...")
    async def sourdough(self, interaction: Interaction, current: int, target: int, leftover: int = 0, ratio: str = "1:1:1", verbose: bool = False):
        try:
            ratio_list = ratio.split(':')
            if (current < 0 or target < 0 or leftover < 0):
                await interaction.response.send_message(content="only positive numbers please... be nice.....")
                return;
        
            if (current == 0):
                await interaction.response.send_message(content="you need to have starter first!")
                return;

            if (target == 0):
                await interaction.response.send_message(content="you don't need any starter? :face_with_raised_eyebrow:")
                return;

            total_target = target + leftover

            if (total_target < current):
                await interaction.response.send_message(content="you already have enough starter! go bake!")
                return;

            if ((len(ratio_list) != 3) or (not all([x.isnumeric() for x in ratio_list])) or (any([int(x) <= 0 for x in ratio_list]))):
                await interaction.response.send_message(content="please input ratio as three positive integers separated by colons, eg. 1:2:3", ephemeral=True)
                return;
            
            int_ratio = [int(x) for x in ratio_list]
            normalized_ratio = [x / int_ratio[0] for x in int_ratio]

            increase = sum(normalized_ratio) / 2

            if (increase <= 1):
                await interaction.response.send_message(content="with the provided ratio of " + ratio + ", your starter will not grow (assuming half is discarded) -- double-check your numbers!", ephemeral=True)
                return;
            
            feedings = math.ceil(math.log(total_target / current, increase))

            total = int(math.pow(increase, feedings) * current)

            message = f"for a recipe requiring {target}g of starter"

            if (leftover > 0):
                message += f" and {leftover}g left over,"

            message += f" you will need to feed {current}g of starter {feedings} times. this will result in {total}g total, leaving {total - target}g left over."

            if (verbose):
                tracker = current
                message += f" [{current}"
                for _ in range(feedings):
                    tracker *= increase 
                    message += f" -> {int(tracker)}"
                message += "]"


            await interaction.response.send_message(message)

        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(SourdoughCommands(bot))
