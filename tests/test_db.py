from unittest.mock import MagicMock, patch

from src.db.db_manager import NotifierDBManager


@patch("db.db_manager.create_engine")
def test_unique_db_engine_when_multiple_instances_calls(create_engine_mock):
    # given
    create_engine_mock.side_effect = [MagicMock(id="mock_1"), MagicMock(id="mock_2")]

    # when - then
    NotifierDBManager()
    assert NotifierDBManager.ENGINE.id == "mock_1"

    NotifierDBManager()
    assert NotifierDBManager.ENGINE.id == "mock_1"
