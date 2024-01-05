# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T
import dataclasses
from pathlib import Path
from datetime import datetime

from .abstraction import AbcProducer
from .record import DataClassRecord
from .buffer import FileBuffer
from .utils import get_utc_now
from .logger import logger


@dataclasses.dataclass
class BaseProducer(AbcProducer):
    """
    todo: docstring
    """

    backoff_wait_time: T.List[int] = dataclasses.field()
    backoff_reset_time: int = dataclasses.field()
    fail_count: int = dataclasses.field()
    first_fail_time: T.Optional[datetime] = dataclasses.field()
    last_fail_time: T.Optional[datetime] = dataclasses.field()
    last_error: T.Optional[Exception] = dataclasses.field()

    def _reset_backoff(self):
        self.fail_count = 0
        self.first_fail_time = None
        self.last_fail_time = None
        self.last_error = None

    def _send(
        self,
        raise_send_error: bool = False,
        _show_backoff: bool = True,
    ):
        """
        This method will be called everytime we put a record to the buffer.

        It checks the exponential backoff to see whether we should try to
        send the emitted records to the sink. If we should, then it takes
        the data from the buffer and call the
        :meth:`abstract_producer.abstraction.AbcProducer.send` method. It also
        handles the exceptions gracefully.
        """
        if _show_backoff:
            logger.info("current backoff status: ")
            with logger.indent():
                logger.info(f"fail_count = {self.fail_count}")
                logger.info(f"first_fail_time = {self.first_fail_time}")
                logger.info(f"last_fail_time = {self.last_fail_time}")
                logger.info(f"last_error = {self.last_error}")

        if self.last_fail_time is None:
            if self.buffer.should_i_emit():
                records = self.buffer.emit()
                try:
                    logger.info(f"📤 send records: {[record.id for record in records]}")
                    self.send(records)
                    logger.info("🟢 task done")
                    self.buffer.task_done()
                    return
                except Exception as e:
                    logger.info(f"🔴 task failed, error: {e!r}")
                    now = get_utc_now()
                    self.fail_count = 1
                    self.first_fail_time = now
                    self.last_fail_time = now
                    self.last_error = e
                    if raise_send_error:
                        raise e
                    return
            else:
                logger.info("🚫 we should not emit")
                return

        now = get_utc_now()

        # failed too many times
        if self.fail_count > len(self.backoff_wait_time):
            logger.info("failed too many times, check if we need to reset backoff ...")
            with logger.indent():
                # beyond reset time
                if (
                    now - self.first_fail_time
                ).total_seconds() >= self.backoff_reset_time:
                    logger.info("yes, reset backoff ...")
                    self._reset_backoff()
                    logger.info("try another time ...")
                    return self._send()
                # do nothing
                else:
                    logger.info("do nothing ...")
                    return

        # when self.fail_count <= len(self.backoff_wait_time)
        if (now - self.first_fail_time).total_seconds() >= self.backoff_wait_time[
            self.fail_count - 1
        ]:
            if self.buffer.should_i_emit():
                records = self.buffer.emit()
                try:
                    logger.info(f"📤 send records: {[record.id for record in records]}")
                    self.send(records)
                    logger.info("🟢 task done")
                    self.buffer.task_done()
                    self._reset_backoff()
                    return
                except Exception as e:
                    logger.info(f"🔴 task failed, error: {e!r}")
                    self.fail_count += 1
                    self.last_fail_time = now
                    self.last_error = e
                    if raise_send_error:
                        raise e
                    return
            else:
                logger.info("🚫 we should not emit")
                return
        else:
            logger.info("🚫 on hold due to exponential backoff")
            return

    @logger.emoji_block(
        msg="put record",
        emoji="📤",
    )
    def _put(
        self,
        record: DataClassRecord,
        raise_send_error: bool = False,
    ):
        logger.info(f"record = {record.serialize()}")
        self.buffer.put(record)
        self._send(
            raise_send_error=raise_send_error,
        )

    def put(
        self,
        record: DataClassRecord,
        raise_send_error: bool = False,
        verbose: bool = False,
    ):
        with logger.disabled(
            disable=not verbose,
        ):
            return self._put(
                record=record,
                raise_send_error=raise_send_error,
            )


@dataclasses.dataclass
class SimpleProducer(BaseProducer):
    """
    This is a very simple producer that write data to a local, append-only file.

    It is a good example to show how to implement a producer and understand the
    behavior of the producer.

    .. note::

        Don't initialize this class directly,
        use the :meth:`SimpleProducer.initialize` method

    See factory method at :meth:`SimpleProducer.new`.
    """

    path: Path = dataclasses.field()
    buffer: FileBuffer = dataclasses.field()

    @classmethod
    def new(
        cls,
        path_sink: Path,
        path_log: Path,
        backoff_wait_time: T.Optional[T.List[int]] = None,
        backoff_reset_time: int = 300,
        max_buffer_records: int = 1000,
        max_buffer_size: int = 1000000,  # 1MB
    ):
        """
        Create a :class:`SimpleProducer` instance.

        :param path_sink: the path of the file you want to write data to.
        :param path_log: the path of the log file you want to persist buffer data.
        :param backoff_wait_time: the wait time of exponential backoff.
        :param backoff_reset_time: the reset time of exponential backoff.
        :param max_buffer_records: the max number of records in the buffer.
        :param max_buffer_size: the max size of the buffer.
        """
        if backoff_wait_time is None:
            backoff_wait_time = [3, 10, 30]
        buffer = FileBuffer(
            record_class=DataClassRecord,
            path=path_log,
            max_records=max_buffer_records,
            max_size=max_buffer_size,
        )
        return cls(
            backoff_wait_time=backoff_wait_time,
            backoff_reset_time=backoff_reset_time,
            fail_count=0,
            first_fail_time=None,
            last_fail_time=None,
            last_error=None,
            path=path_sink,
            buffer=buffer,
        )

    def send(self, records: T.List[DataClassRecord]):
        with self.path.open("a") as f:
            for record in records:
                f.write(record.serialize() + "\n")

    def get_all_records(self) -> T.List[DataClassRecord]:
        records = list()
        if self.path.exists():
            records.extend(self.buffer._read_log_files(self.path))
        for path in self.buffer._get_old_log_files():
            records.extend(self.buffer._read_log_files(path))
        if self.buffer.path.exists():
            records.extend(self.buffer._read_log_files(self.buffer.path))
        return records
