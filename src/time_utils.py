import datetime
import pytz


def to_ist_iso8601(dt: datetime.datetime) -> str:
    """
    Convert a datetime object to ISO 8601 string in IST timezone.
    """
    ist = pytz.timezone("Asia/Kolkata")
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    dt_ist = dt.astimezone(ist)
    return dt_ist.isoformat()

def parse_iso8601_to_ist(dt_str: str) -> datetime.datetime:
    """
    Parse an ISO 8601 datetime string and convert to IST timezone.
    """
    dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    ist = pytz.timezone("Asia/Kolkata")
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(ist)

def get_ist_now() -> str:
    """
    Get the current date and time in IST timezone.
    """
    return to_ist_iso8601(datetime.datetime.now(pytz.timezone("Asia/Kolkata")))