from datetime import datetime
from enum import Enum

import pytz


# DAYS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class TimeZones(Enum):
    AMSTERDAM = "Europe/Amsterdam"
    BSAS = "America/Argentina/Buenos_Aires"


def get_time_in_time_zone(utc_date: datetime, time_zone: TimeZones) -> datetime:
    required_tz = pytz.timezone(time_zone.value)
    required_tz_dt = utc_date.replace(tzinfo=pytz.utc).astimezone(required_tz)
    return required_tz.normalize(required_tz_dt)
