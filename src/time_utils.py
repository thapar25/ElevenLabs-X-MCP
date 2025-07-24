import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def to_ist_iso8601(dt: datetime.datetime) -> str:
    """
    Convert a datetime object to ISO 8601 string in IST timezone.
    """
    if dt.tzinfo is None:
        dt = IST.localize(dt)
    else:
        dt = dt.astimezone(IST)
    return dt.isoformat()


def parse_iso8601_to_ist(dt_str: str) -> datetime.datetime:
    """
    Parse an ISO 8601 datetime string and ensure it's in IST timezone.
    Assumes input is always IST, but naive (no tzinfo).
    """
    dt = datetime.datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = IST.localize(dt)
    else:
        dt = dt.astimezone(IST)
    return dt
