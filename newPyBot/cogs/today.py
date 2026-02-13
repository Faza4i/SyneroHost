import disnake
from disnake.ext import commands
from datetime import datetime, date

class Today(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="today", description="Показать сколько дней прошло")
    async def today(self, inter: disnake.ApplicationCommandInteraction):

        start_date = date(2023, 12, 29)
        today = date.today()
        days_passed = (today - start_date).days

        unix_timestamp = int(datetime(start_date.year, start_date.month, start_date.day).timestamp())

        embed = disnake.Embed(
            title="💖 Важная дата",
            description=(
                f"Я тебя люблю уже **{days_passed}** дней.\n\n"
                f"<t:{unix_timestamp}:D>."
            ),
            color=disnake.Color.from_rgb(161, 36, 52)  # мягкий бордовый
        )
        await inter.response.send_message(embed=embed)
        

def setup(bot):
    bot.add_cog(Today(bot))