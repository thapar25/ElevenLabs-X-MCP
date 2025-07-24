import datetime
import pytz


def format_dt(dt_str):
    """Format the datetime string to a more readable format."""
    if "T" in dt_str:
        # Always handle Zulu time
        if dt_str.endswith("Z"):
            dt_str = dt_str.replace("Z", "+00:00")
        try:
            dt = datetime.datetime.fromisoformat(dt_str)
        except ValueError:
            return dt_str  # fallback: return as-is if parsing fails
        # Convert to IST for display
        ist = pytz.timezone("Asia/Kolkata")
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        dt_ist = dt.astimezone(ist)
        return dt_ist.strftime("%A, %d %B %Y %I:%M %p (IST)")
    return dt_str


def to_rfc3339(dt_str: str, default_tz="UTC") -> str:
    """
    Convert a datetime string to RFC 3339 format with timezone.
    Assumes input is in 'YYYY-MM-DD HH:MM' or ISO format.
    """
    try:
        # Try ISO format first
        dt = datetime.datetime.fromisoformat(dt_str)
    except ValueError:
        # Fallback to 'YYYY-MM-DD HH:MM' format
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    if dt.tzinfo is None:
        tz = pytz.timezone(default_tz)
        dt = tz.localize(dt)
    return dt.isoformat()
