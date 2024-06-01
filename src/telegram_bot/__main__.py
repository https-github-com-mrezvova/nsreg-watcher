import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
import subprocess
import os


current_directory = os.getcwd()
TOKEN = os.environ["BOT_TOKEN"]
ERROR_LOGS_PATH = "logs/grabber_errors.log"
CHAT_ID = os.environ["CHAT_ID"]
TOPIC_SUPPORT_ID = int(os.environ["TOPIC_SUPPORT_ID"])

if current_directory == '/home/ecodomen/ecodomen-dev/src/telegram_bot/':
    SPIDERS_SCRIPT_PATH = "compose/scrapy/scrapy-dev.sh"
    SERVER = "DEV-SERVER"
else:
    SPIDERS_SCRIPT_PATH = "compose/scrapy/scrapy-prod.sh"
    SERVER = "PROD-SERVER"

router = Router()
bot = Bot(TOKEN, parse_mode="markdown")
bot_is_done = False


def cut_log(log: str) -> str:
    """Make log shorter if len > 4000"""
    log = log.split("---SPLIT---")[-1]
    if len(log) > 4000:
        log = f"{log[:4001]}..."
    return log


@router.message(Command(commands=["start"]))
async def command_start_handler(*args, **kwargs) -> None:
    await bot.send_message(
        chat_id=CHAT_ID,
        message_thread_id=TOPIC_SUPPORT_ID,
        text=f"🕷️🕷️🕷️ Запуск спайдеров - {SERVER} 🕷️🕷️🕷️"
    )
    try:
        subprocess.run(["sh", f"{SPIDERS_SCRIPT_PATH}"], check=True)

        with open(ERROR_LOGS_PATH) as file:
            error_log = file.read()

        error_log = cut_log(error_log)
        spider_1 = r'/╲/\(╭•̀ﮧ •́╮)/\╱\ '

        await bot.send_message(
            chat_id=CHAT_ID,
            message_thread_id=TOPIC_SUPPORT_ID,
            text=f"Спайдеры завершили свою работу {spider_1}\nError logs:\n```{error_log}```"
        )

    except subprocess.CalledProcessError as error:
        spider_2 = r"/╲/\╭[ ☉ ﹏ ☉ ]╮/\╱\ "
        await bot.send_message(
            chat_id=CHAT_ID,
            message_thread_id=TOPIC_SUPPORT_ID,
            text=f"{spider_2}\n{error}"
        )


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    await command_start_handler()

    # Only start polling if the bot should still be active
    if not bot_is_done:
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
