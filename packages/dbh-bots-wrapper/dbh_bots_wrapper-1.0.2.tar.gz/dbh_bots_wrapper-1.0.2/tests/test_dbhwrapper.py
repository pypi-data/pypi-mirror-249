# tests/test_dbhwrapper.py

from dbh-bots-wrapper import bot
from pytest import fixture

@fixture
def test_addbot():
    """Tests an API call to send a bot adding request"""
    bot_instance = bot(
        "748317979971682385",
        "915989266943860746",
        "amongusbot",
        1,
        1,
        1,
    )
    res = bot_instance.info()
    
    assert isinstance(res, dict)
    assert response['discord_id'] == "748317979971682385"

## i want to write more tests but im lazy so no