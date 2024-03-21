from random import randrange
from datetime import timedelta, datetime, timezone

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
UTC_OFFSET = "+00:00"
FLOOR_DATETIME = "2014-01-01 01:30:00.000000"
CEIL_DATETIME = "2024-03-21 03:19:28.999999"

def to_seconds(days):
    return days * 24 * 60 * 60

def generate_random_datetime(start, end, time_format):
    """
    This function will return a random datetime between two datetime 
    strings.
    """
    start_datetime = datetime.strptime(start, time_format)
    end_datetime = datetime.strptime(end, time_format)
    delta = end_datetime - start_datetime
    int_delta = to_seconds(delta.days) + delta.seconds
    random_second = randrange(int_delta)
    random_microsecond = randrange(delta.microseconds)
    t = start_datetime + timedelta(seconds=random_second, microseconds=random_microsecond)
    return t.replace(tzinfo=timezone.utc)

def random_datetime():
    return generate_random_datetime(FLOOR_DATETIME, CEIL_DATETIME, DATETIME_FORMAT)
