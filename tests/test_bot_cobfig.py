from unittest.mock import patch

import pytest

from src.telegram_bot.config import BotConfig, load_bot_config


def test_bot_config():
    config = {"bot_token": "111", "chat_id": "222", "topic_id": "333"}
    bot_config = BotConfig(**config)

    assert bot_config.bot_token == config["bot_token"]
    assert bot_config.chat_id == config["chat_id"]
    assert bot_config.topic_id == config["topic_id"]


@pytest.mark.parametrize(
    "config",
    [
        {"chat_id": "222", "topic_id": "333"},
        {"bot_token": "111", "topic_id": "333"},
        {"bot_token": "111", "chat_id": "222"},
        {},
    ],
)
def test_bot_config_missing_params(config):
    with pytest.raises(TypeError):
        BotConfig(**config)


@patch.dict(
    "os.environ",
    {"BOT_TOKEN": "111", "CHAT_ID": "222", "TOPIC_SUPPORT_ID": "333"},
)
def test_load_bot_config():
    expected_config = BotConfig(
        bot_token="111",
        chat_id="222",
        topic_id="333",
    )
    config = load_bot_config()
    assert config == expected_config


@patch.dict("os.environ")
def test_load_bot_config_missing_topic_id():
    with pytest.raises(KeyError):
        load_bot_config()
