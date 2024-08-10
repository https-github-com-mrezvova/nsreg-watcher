import logging
import os
from dataclasses import dataclass


logger = logging.getLogger(__name__)

BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"
TOPIC_SUPPORT_ID = "TOPIC_SUPPORT_ID"


@dataclass
class BotConfig:
    bot_token: str
    chat_id: str
    topic_id: str
    # TODO: Передать config парсера с (log_path, log_file_postfix, lod_age_max)
    log_path: str = "logs/"
    log_file_postfix: str = "_grabber_errors.log"
    lod_max_age: int = 5


def get_env_value(name: str) -> str:
    value = os.getenv(name)
    if not value:
        msg = f"Environment variable '{name}' not set"
        logger.critical(msg)
        raise KeyError(msg)
    return value


def load_bot_config() -> BotConfig:
    bot_token = get_env_value(BOT_TOKEN)
    chat_id = get_env_value(CHAT_ID)
    topic_id = get_env_value(TOPIC_SUPPORT_ID)
    return BotConfig(
        bot_token=bot_token,
        chat_id=chat_id,
        topic_id=topic_id,
    )
