# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T
import dataclasses
from pathlib import Path

from ..vendor.aws_cloudwatch_logs_insights_query import (
    Event,
    put_log_events,
    get_ts_in_millisecond,
)

from ..abstraction import T_RECORD
from ..record import DataClassRecord
from ..buffer import FileBuffer
from ..producer import BaseProducer

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


@dataclasses.dataclass
class AwsCloudWatchLogsProducer(BaseProducer):
    """
    This producer sends the records to AWS CloudWatch Logs.

    See factory method at :meth:`AwsCloudWatchLogsProducer.new`.
    """

    bsm: "BotoSesManager" = dataclasses.field()
    log_group_name: str = dataclasses.field()
    log_stream_name: str = dataclasses.field()
    buffer: FileBuffer = dataclasses.field()

    @classmethod
    def new(
        cls,
        record_class: T.Type[T_RECORD],
        bsm: "BotoSesManager",
        log_group_name: str,
        log_stream_name: str,
        path_log: Path,
        backoff_wait_time: T.Optional[T.List[int]] = None,
        backoff_reset_time: int = 300,
        max_buffer_records: int = 1000,
        max_buffer_size: int = 1000000,  # 1MB
    ):
        """
        Create a :class:`AwsCloudWatchLogsProducer` instance.

        :param record_class: The record class to use.
        :param bsm: the boto session manager object
        :param log_group_name: the name of the log group
        :param log_stream_name: the name of the log stream
        :param path_log: the path of the log file you want to persist buffer data.
        :param backoff_wait_time: the wait time of exponential backoff.
        :param backoff_reset_time: the reset time of exponential backoff.
        :param max_buffer_records: the max number of records in the buffer.
        :param max_buffer_size: the max size of the buffer.
        """
        if backoff_wait_time is None:
            backoff_wait_time = [3, 10, 30]
        buffer = FileBuffer(
            record_class=record_class,
            path=path_log,
            max_records=max_buffer_records,
            max_size=max_buffer_size,
        )
        return cls(
            bsm=bsm,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
            backoff_wait_time=backoff_wait_time,
            backoff_reset_time=backoff_reset_time,
            fail_count=0,
            first_fail_time=None,
            last_fail_time=None,
            last_error=None,
            buffer=buffer,
        )

    def send(self, records: T.List[T_RECORD]):
        events = [
            Event(
                message=record.serialize(),
                timestamp=get_ts_in_millisecond(record.create_at_dt),
            )
            for record in records
        ]
        return put_log_events(
            logs_client=self.bsm.cloudwatchlogs_client,
            group_name=self.log_group_name,
            stream_name=self.log_stream_name,
            events=events,
        )
