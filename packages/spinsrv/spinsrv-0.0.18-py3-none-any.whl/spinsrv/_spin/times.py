import datetime

"""
    Time represents a timestamp, in units of *micro*seconds,
    since the Unix epoch, Jan 1 1970 0:00 UTC.
"""
Time = int


def now() -> Time:
    return time_from_python(datetime.datetime.now(tz=datetime.timezone.utc))


def python_time(t: Time) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(t / 1_000_000, tz=datetime.timezone.utc)


def time_from_python(t: datetime.datetime) -> Time:
    return int(t.timestamp() * 1_000_000)
