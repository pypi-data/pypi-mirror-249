import pytz
from datetime import datetime

from .decouple import config


def make_aware(date_time: datetime = None) -> datetime:
    timezone = pytz.timezone(config('TIME_ZONE', default='Africa/Dar_Es_Salaam'))
    return timezone.localize(date_time, is_dst=True)
