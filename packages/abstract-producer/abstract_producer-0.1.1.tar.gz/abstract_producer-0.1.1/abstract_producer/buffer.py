# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T
import sys
import random
import collections
from pathlib import Path
from datetime import datetime, timezone

from .abstraction import AbcBuffer, T_RECORD
from .exc import BufferIsEmptyError


class BaseBuffer(AbcBuffer):
    """
    todo: docstring
    """
    pass


_FILENAME_FRIENDLY_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S_%f"


class FileBuffer(BaseBuffer):
    """
    Use local log file as write-ahead-log (WAL) to persist the buffer.

    See factory method at :meth:`FileBuffer.new`.
    """
    def __init__(
        self,
        record_class: T.Type[T_RECORD],
        path: Path,
        max_records: int = 1000,
        max_size: int = 1000000,  # KB
    ):
        self.record_class = record_class
        self.path = path
        self.max_records = max_records
        self.max_size = max_size

        self._current_records = 0
        self._current_size = 0

        self._mem_serialized_queue: T.Deque[str] = collections.deque()
        self._mem_queue: T.Deque[T_RECORD] = collections.deque()
        self._file_queue: T.Deque[Path] = collections.deque()

        self._validate_path()

    def _read_log_files(self, path: Path) -> T.List[T_RECORD]:
        """
        Load records from one log file.
        """
        return [
            self.record_class.deserialize(line)
            for line in path.read_text().splitlines()
        ]

    def _get_new_log_file(self, create_at_dt: datetime) -> Path:
        """
        Get the path of the new log file to persist the buffer.
        """
        utc_create_at_dt = create_at_dt.astimezone(timezone.utc)
        dt_str = utc_create_at_dt.strftime(_FILENAME_FRIENDLY_DATETIME_FORMAT)
        return self.path.parent.joinpath(f"{self.path.stem}.{dt_str}{self.path.suffix}")

    def _get_old_log_files(self) -> T.List[Path]:
        """
        Get the path of the old log files. Their file name looks like::

            ${prefix}.${timestamp}.${suffix}
        """
        prefix = self.path.stem + "."
        suffix = self.path.suffix
        path_list = list()
        for p in self.path.parent.iterdir():
            # fmt: off
            if (
                (p.name.startswith(prefix) and p.name.endswith(suffix))
                and p != self.path
            ):
            # fmt: on
                path_list.append(p)
        path_list.sort()
        return path_list

    def _push(self, record: T_RECORD):
        data = record.serialize()
        self._mem_serialized_queue.appendleft(data)
        self._mem_queue.appendleft(record)
        self._current_records += 1
        self._current_size += sys.getsizeof(data)

    def _push_many(self, records: T.Iterable[T_RECORD]):
        for record in records:
            self._push(record)

    def _validate_path(self):
        """
        Locate all persisted log files and check if the number of records in each file
        match the ``max_size``.
        """
        #
        if self.path.exists():
            records = self._read_log_files(self.path)
            if len(records) >= self.max_records:  # pragma: no cover
                raise ValueError("you should not change max_size!")
            self._push_many(records)

        #
        path_list = self._get_old_log_files()

        if len(path_list):
            n_records = len(random.choice(path_list).read_text().splitlines())
            if n_records != self.max_records:  # pragma: no cover
                raise ValueError("you should not change max_size!")
        self._file_queue.extendleft(path_list)

    @classmethod
    def new(
        cls,
        record_class: T.Type[T_RECORD],
        path: Path,
        max_records: int = 1000,
        max_size: int = 1000000,
    ):
        """
        :param record_class: the record class.
        :param path: the path of the log file. for example: ``my_buffer.log``
        :param max_records: Max number of records that can be stored in the buffer.
        :param max_size: Max total size of records (in bytes) that can be stored in the buffer.
        """
        return cls(
            record_class=record_class,
            path=path,
            max_records=max_records,
            max_size=max_size,
        )

    def clear_memory_queue(self):
        self._current_size = 0
        self._current_records = 0
        self._mem_serialized_queue.clear()
        self._mem_queue.clear()

    @property
    def queue(self):
        return self._mem_queue

    def clear_queue(self):  # pragma: no cover
        self._mem_queue.clear()

    def clear_persistent(self):
        # remove all log files and file queue
        prefix = self.path.stem + "."
        suffix = self.path.suffix
        for p in self.path.parent.iterdir():
            if (
                p.name.startswith(prefix) and p.name.endswith(suffix)
            ) or p == self.path:
                p.unlink()
        self._file_queue.clear()
        # clear memory queue
        self.clear_memory_queue()

    def put(self, record: T_RECORD):
        # immediately append to log file
        # todo: when putting lots of records, avoid open and close file every time, maybe create a put_many method
        self._push(record)
        with self.path.open("a") as f:
            f.write(self._mem_serialized_queue[0] + "\n")

        # when buffer is full, create a new log file and clear the memory queue
        # print(f"{self._current_records = }, {self.max_records = }, {self._current_size = }, {self.max_size = }")
        if (
            self._current_records == self.max_records
            or self._current_size >= self.max_size
        ):
            path = self._get_new_log_file(self._mem_queue[0].create_at_dt)
            self.path.rename(path)
            self._file_queue.appendleft(path)
            self.clear_memory_queue()

    def should_i_emit(self) -> bool:
        return len(self._file_queue) > 0

    def emit(self) -> T.List[T_RECORD]:
        if self._file_queue:
            records = self._read_log_files(self._file_queue[-1])
            return records
        elif self._mem_queue:
            return list(self._mem_queue)
        else:
            raise BufferIsEmptyError

    def task_done(self):
        if self._file_queue:
            self._file_queue.pop().unlink()
        elif self._mem_queue:
            self.clear_memory_queue()
            self.path.unlink()
        else:
            raise BufferIsEmptyError
