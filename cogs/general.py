import disnake
from disnake.ext import commands


class General(commands.Cog):
    """Basic slash and prefix commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("General cog loaded.")


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))

