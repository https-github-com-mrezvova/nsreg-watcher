import tempfile

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.telegram_bot.services.file_services import LogFilesService


@pytest.fixture
def mock_bot():
    return MagicMock()


@pytest.fixture
def mock_config():
    return MagicMock()


@pytest.fixture
def mock_os():
    return MagicMock()


@pytest.fixture
def log_files_service(mock_bot, mock_config):
    return LogFilesService(mock_bot, mock_config)


@pytest.mark.asyncio
async def test_get_today_grabber_log_file(
    log_files_service, mock_bot, mock_config, mock_os
):
    mock_bot.send_message = AsyncMock()
    with patch("os.path.exists", return_value=True):
        await log_files_service._set_today_log_file_path()

    assert log_files_service._log_file is not None


@pytest.mark.asyncio
async def test_get_today_grabber_log_file_none_exist(
    log_files_service, mock_bot, mock_config, mock_os
):
    mock_bot.send_message = AsyncMock()

    await log_files_service._set_today_log_file_path()
    assert log_files_service._log_file is None


@pytest.mark.asyncio
async def test_read_log_file(log_files_service, mock_bot, mock_config):
    with tempfile.NamedTemporaryFile() as temp_file:
        log_files_service._log_file = temp_file.name
        mock_bot.send_message = AsyncMock()

        await log_files_service._check_log_file_size()
        assert log_files_service._log_empty is True


@pytest.mark.asyncio
async def test_read_log_file_non_empty(log_files_service, mock_bot, mock_config):
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(b"Some content")
        temp_file.flush()
        log_files_service._log_file = temp_file.name
        mock_bot.send_message = AsyncMock()

        await log_files_service._check_log_file_size()
        assert log_files_service._log_empty is False


@pytest.mark.asyncio
async def test_send_log_file(log_files_service, mock_bot, mock_config):
    log_files_service._log_file = "existing_log.log"
    mock_bot.send_document = AsyncMock()

    await log_files_service._send_log_file()
    assert log_files_service._log_has_been_sent is True
