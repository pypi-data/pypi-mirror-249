# -*- coding: utf-8 -*-

"""
Usage example::

    >>> import abstract_producer.api as abstract_producer

    >>> abstract_producer.DataClassRecord
    >>> abstract_producer.FileBuffer
    >>> abstract_producer.SimpleProducer
"""

from .abstraction import T_RECORD
from .abstraction import T_BUFFER
from .abstraction import T_PRODUCER
from .record import BaseRecord
from .record import DataClassRecord
from .buffer import BaseBuffer
from .buffer import FileBuffer
from .producer import BaseProducer
from .producer import SimpleProducer
from . import exc
from . import utils

try:
    from .producers.aws_cloudwatch_logs import AwsCloudWatchLogsProducer
except ImportError:  # pragma: no cover
    pass
