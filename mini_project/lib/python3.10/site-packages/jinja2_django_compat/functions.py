import datetime

from django.conf import settings
from django.utils import timezone


def now(format_string):
    tzinfo = timezone.get_current_timezone() if settings.USE_TZ else None
    return datetime.date(datetime.now(tz=tzinfo), format_string)
