import json as jsonlib
import re
import time
import unittest.mock as mock
from pathlib import Path

import pytest

from yatbaf.models import UpdateInfo
from yatbaf.router import OnMessage
from yatbaf.types import Chat
from yatbaf.types import Message
from yatbaf.types import Update
from yatbaf.types import User


@pytest.fixture
def token():
    return "12345678:testtoken"


@pytest.fixture
def handler():
    return mock.AsyncMock(return_value=None)


@pytest.fixture
def user():
    return User(
        id=1010,
        username="testuser",
        is_bot=False,
        first_name="Test",
    )


@pytest.fixture
def chat():
    return Chat(
        id=101010,
        type="group",
        username="testchat",
    )


@pytest.fixture
def message(chat, user):
    return Message(
        from_=user,
        chat=chat,
        date=int(time.time()),
        message_id=101010,
    )


@pytest.fixture
def update(message):
    return Update(
        update_id=9999,
        message=message,
    )


@pytest.fixture
def update_info(update):
    return UpdateInfo(
        id=update.update_id,
        content=update.message,
        name="message",
    )


@pytest.fixture
def router():
    return OnMessage()


# yapf: disable
@pytest.fixture
def asyncdef():
    def factory(result=None):
        async def func(*_, **__):  # noqa: U101
            return result
        return func
    return factory
    # yapf: enable


@pytest.fixture(scope="session")
def api_spec():
    api_json_file = Path(__file__).parent / "data" / "api.json"
    with api_json_file.open("rb") as f:
        return jsonlib.load(f)


def _capitalize(w):
    return f"{w[0].upper()}{w[1:]}"


def _snake_case(s):
    return '_'.join(
        re.sub(
            '([A-Z][a-z]+)',
            r' \1',
            re.sub('([A-Z]+)', r' \1', s.replace('-', ' '))
        ).split()
    ).lower()


@pytest.fixture
def capitalize():
    return _capitalize


@pytest.fixture
def snake_case():
    return _snake_case
