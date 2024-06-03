import logging
import os
from datetime import datetime, timedelta

import aiofiles
from aiogram import Bot
from aiogram.types import FSInputFile

from src.telegram_bot.config import BotConfig

logger = logging.getLogger(__name__)


class LogFilesService:
    def __init__(self, bot: Bot, config: BotConfig):
        self._bot = bot
        self._config = config
        self._log_file = None
        self._log_empty = True
        self._log_has_been_sent = False

    async def _get_today_grabber_log_file(self) -> None:
        today_log_file_name = (
            datetime.now().strftime("%Y-%m-%d") + self._config.log_file_postfix
        )
        path = os.path.join(self._config.log_path, today_log_file_name)
        if not os.path.exists(path):
            msg = (
                f"Log file '{today_log_file_name}' not found."
                f"\nCheck if the parser is working properly."
            )
            logger.error(msg)
            await self._bot.send_message(
                chat_id=self._config.chat_id,
                message_thread_id=int(self._config.topic_id),
                text=msg,
            )
            return
        self._log_file = path

    async def _read_log_file(self) -> None:
        async with aiofiles.open(self._log_file, "rb") as file:
            lines = await file.read()
        if lines:
            self._log_empty = False
            return
        msg = "Log file is empty."
        logger.info(msg)
        await self._bot.send_message(
            chat_id=self._config.chat_id,
            message_thread_id=int(self._config.topic_id),
            text=msg,
        )

    async def _send_log_file(self) -> None:
        try:
            msg = "Log file."
            await self._bot.send_document(
                chat_id=self._config.chat_id,
                message_thread_id=int(self._config.topic_id),
                document=FSInputFile(self._log_file),
                caption=msg,
            )
            logger.info("Log file sent.")
            self._log_has_been_sent = True
        except Exception as err:
            logger.error(err)
            await self._bot.send_message(
                chat_id=self._config.chat_id,
                message_thread_id=int(self._config.topic_id),
                text=str(err),
            )

    async def _delete_old_log_files(self):
        current_date = datetime.now()
        for file in os.listdir(self._config.log_path):
            file_path = os.path.join(self._config.log_path, file)
            if os.path.isfile(file_path) and file.endswith(".log"):
                creation_date = datetime.fromtimestamp(
                    os.stat(file_path).st_ctime
                )
                age = current_date - creation_date
                msg = f"Deleted old log file '{file_path}'"
                if age > timedelta(days=self._config.lod_max_age):
                    os.remove(file_path)
                    logger.debug(msg)

    async def grabber_log_processor(self) -> None:
        await self._get_today_grabber_log_file()
        if self._log_file:
            await self._read_log_file()
        if not self._log_empty:
            await self._send_log_file()
        if self._log_has_been_sent:
            await self._delete_old_log_files()
