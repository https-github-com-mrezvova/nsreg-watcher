import logging
import os
from datetime import datetime, timedelta

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

    async def _set_today_log_file_path(self) -> None:
        today_log_file_name = (
            datetime.now().strftime("%Y-%m-%d") + self._config.log_file_postfix
        )
        file_path = os.path.join(self._config.log_path, today_log_file_name)
        if not os.path.exists(file_path):
            msg = (
                f"Log file '{today_log_file_name}' not found."
                f"\nCheck if the parser is working properly."
            )
            logger.warning(msg)
            await self._bot.send_message(
                chat_id=self._config.chat_id,
                message_thread_id=int(self._config.topic_id),
                text=msg,
            )
            return
        self._log_file = file_path

    async def _check_log_file_size(self) -> None:
        if os.path.getsize(self._log_file) > 0:
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
            await self._bot.send_document(
                chat_id=self._config.chat_id,
                message_thread_id=int(self._config.topic_id),
                document=FSInputFile(self._log_file),
                caption="Log file",
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

    async def _delete_old_log_files(self) -> None:
        current_date = datetime.now()
        for file in os.listdir(self._config.log_path):
            file_path = os.path.join(self._config.log_path, file)
            if os.path.isfile(file_path) and file.endswith(".log"):
                creation_date = datetime.fromtimestamp(
                    os.stat(file_path).st_ctime
                )
                age = current_date - creation_date
                if age > timedelta(days=self._config.lod_max_age):
                    os.remove(file_path)
                    logger.debug(f"Deleted old log file '{file_path}'")

    async def grabber_log_processor(self) -> None:
        await self._set_today_log_file_path()
        if self._log_file:
            await self._check_log_file_size()
        if not self._log_empty:
            await self._send_log_file()
        if self._log_has_been_sent:
            await self._delete_old_log_files()
