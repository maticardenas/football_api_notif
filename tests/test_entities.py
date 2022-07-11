from datetime import datetime

from src.entities import Fixture
from src.utils.date_utils import get_time_in_time_zone, TimeZones


def test_fixture_post_init(fixture: Fixture):
    # given - when - then
    assert fixture.is_next_day == ""
    assert fixture.futbol_libre_url == "https://futbollibre.net"
    assert fixture.futbol_para_todos_url == "https://futbolparatodos.online/es/"
    assert fixture.line_up == None
    assert fixture.highlights == [
        f"https://www.youtube.com/results?search_query=River Plate+vs+Boca "
        f"Juniors+jugadas+resumen"
    ]
    assert fixture.head_to_head == []


def test_matched_played_str(fixture: Fixture):
    # given - when - then
    assert (
        fixture.matched_played_str()
        == """⚽ *River Plate - 3 vs. 0 - Boca Juniors*
🏆 *Copa de la Superliga*
📌 *Primera Fecha*"""
    )


def test_time_telegram_text(fixture: Fixture):
    # given - when - then
    assert (
        fixture.time_telegram_text()
        == "🇪🇺 <strong>16:00 HS </strong> / 🇦🇷 <strong>12:00 "
        "HS</strong>"
    )


def test_one_line_telegram_repr(fixture: Fixture):
    # given - when - then
    assert (
        fixture.one_line_telegram_repr()
        == """⚽ <strong>River Plate vs. Boca Juniors</strong> 
🏆 <strong>Copa de la Superliga</strong>
⏰ 🇪🇺 <strong>16:00 HS </strong> / 🇦🇷 <strong>12:00 HS</strong>"""
    )


def test_telegram_like_repr(fixture: Fixture):
    # given - when - then
    fixture.telegram_like_repr() == """🇪🇺 <strong>16:00 HS </strong>
🇦🇷 <strong>12:00 HS</strong>

⏰ Faltan 0 minutos para el partido.

⚽ <strong>River Plate vs. Boca Juniors</strong>
🏆 <strong>Copa de la Superliga</strong>

📺 <a href='https://futbollibre.net'>Streaming Online (FutbolLibre)</a>
📺 <a href='https://futbollibre.net'>Streaming Online (FPT)</a>"""


def test_matched_played_telegram_like_repr(fixture: Fixture):
    # given - when - then
    fixture.matched_played_telegram_like_repr() == """<strong>⚽ River Plate 
    [3] vs.  [0] Boca Juniors</strong>
🏆 <strong>Copa de la Superliga</strong>
📌 <strong>Primera Fecha</strong>

"""


def test_is_next_day_in_europe(fixture: Fixture):
    # given - when - then
    assert fixture._is_next_day_in_europe() == False


def test_is_next_day_in_europe_true(fixture: Fixture):
    # given
    next_day_date = datetime.strptime("2019-01-02T15:00:00", "%Y-%m-%dT%H:%M:%S")
    fixture.ams_date = get_time_in_time_zone(next_day_date, TimeZones.AMSTERDAM)

    # when - then
    assert fixture._is_next_day_in_europe() == True
