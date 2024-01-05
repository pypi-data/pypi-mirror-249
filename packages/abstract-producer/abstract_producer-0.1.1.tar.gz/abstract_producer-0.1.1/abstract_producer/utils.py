# -*- coding: utf-8 -*-

import uuid
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)
