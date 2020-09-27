from datetime import datetime
from typing import Optional


def valid_time_hhmm(raid_time: str) -> Optional[datetime]:
    try:
        assert (int(raid_time.replace(":", "").replace(".", "").replace(";", "")) < 2400)
        return datetime.strptime(raid_time, "%H:%M")
    except:
        return _maybe_fix_valid_hhmm(raid_time)


def _maybe_fix_valid_hhmm(raid_time: str) -> Optional[datetime]:
    try:
        raid_time = raid_time.replace(".", ":").replace(";", ":")
        if len(raid_time) == 4:
            if ":" not in raid_time:
                raid_time = f"{raid_time[:2]}:{raid_time[2:]}"
            elif raid_time[1] == ":":
                raid_time = f"0{raid_time}"
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