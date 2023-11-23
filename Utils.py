
from datetime import datetime, timedelta


def week2date(week: int) -> str:
    """Returns the date of the first day of the given week."""
    return (datetime(2023, 11, 26) + timedelta(days=7 * (week - 1))).isoformat()