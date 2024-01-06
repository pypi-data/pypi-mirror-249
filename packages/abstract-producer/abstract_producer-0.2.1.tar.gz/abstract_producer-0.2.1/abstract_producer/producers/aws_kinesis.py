# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T
import base64
import dataclasses
from pathlib import Path

from ..abstraction import T_RECORD
from ..buffer import FileBuffer
from ..producer import BaseProducer

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


@dataclasses.dataclass
class AwsKinesisStreamProducer(BaseProducer):
    """
    This producer sends the records to AWS Kinesis Stream.

    See factory method at :meth:`AwsKinesisStreamProducer.new`.
    """

    bsm: "BotoSesManager" = dataclasses.field()
    stream_name: str = dataclasses.field()
    buffer: FileBuffer = dataclasses.field()

    @classmethod
    def new(
        cls,
        record_class: T.Type[T_RECORD],
        bsm: "BotoSesManager",
        stream_name: str,
        path_log: Path,
        backoff_wait_time: T.Optional[T.List[int]] = None,
        backoff_reset_time: int = 300,
        max_buffer_records: int = 1000,
        max_buffer_size: int = 1000000,  # 1MB
    ):
        """
        Create a :class:`AwsKinesisStreamProducer` instance.

        :param record_class: The record class to use.
        :param bsm: the boto session manager object
        :param stream_name: the name of the kinesis stream
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
            stream_name=stream_name,
            backoff_wait_time=backoff_wait_time,
            backoff_reset_time=backoff_reset_time,
            fail_count=0,
            first_fail_time=None,
            last_fail_time=None,
            last_error=None,
            buffer=buffer,
        )

    def send(self, records: T.List[T_RECORD]):
        """
        Send records to AWS Kinesis Stream.
        """
        return self.bsm.kinesis_client.put_records(
            Records=[
                dict(
                    Data=base64.b64encode(record.serialize().encode("utf-8")),
                    PartitionKey="server_1",
                )
                for record in records
            ],
            StreamName=self.stream_name,
        )
