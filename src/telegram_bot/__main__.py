import asyncio
import logging

from aiogram import Bot

from src.telegram_bot.config import load_bot_config
from src.telegram_bot.services.file_services import LogFilesService

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Bot start")
    config = load_bot_config()
    bot = Bot(config.bot_token)
    services = LogFilesService(bot, config)
    await services.grabber_log_processor()
    await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.exception("Bot stop")
