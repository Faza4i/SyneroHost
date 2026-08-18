import os
import asyncio
from pathlib import Path

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from aiohttp import web

BASE_DIR = Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"


# --- Фейковый веб-сервер для проходимости Health Check на Render ---
async def handle_ping(request):
    return web.Response(text="Bot is alive!", status=200)

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render автоматически передает случайный номер порта в $PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")


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


async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Set DISCORD_TOKEN in your environment or .env file.")

    # 1. Запускаем веб-сервер, чтобы Render прошёл сканирование портов
    await start_web_server()

    # 2. Запускаем бота через асинхронный старт вместо bot.run()
    bot = create_bot()
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
