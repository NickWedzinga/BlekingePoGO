from typing import Optional
from datetime import datetime


def valid_time_hhmm(raid_time: str) -> Optional[datetime]:
    try:
        assert (int(raid_time.replace(":", "")) < 2400)
        return datetime.strptime(raid_time, "%H:%M")
    except:
        return None


def valid_time_mm(raid_time: str) -> Optional[datetime]:
    try:
        assert (int(raid_time) < 60)
        return datetime.strptime(raid_time, "%M")
    except:
        return None


def format_as_hhmm(time: datetime) -> str:
    """Converts a datetime into HH:MM"""
    return '{:%H:%M}'.format(time)