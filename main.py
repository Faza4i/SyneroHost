import os
from pathlib import Path

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"


def create_bot() -> commands.Bot:
    load_dotenv()

    intents = disnake.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    for cog_file in COGS_DIR.glob("*.py"):
        if cog_file.name.startswith("_"):
            continue
        extension = f"cogs.{cog_file.stem}"
        bot.load_extension(extension)
        print(f"Loaded extension: {extension}")

    return bot


if __name__ == "__main__":
    bot = create_bot()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Set DISCORD_TOKEN in your environment or .env file.")
    bot.run(token)

