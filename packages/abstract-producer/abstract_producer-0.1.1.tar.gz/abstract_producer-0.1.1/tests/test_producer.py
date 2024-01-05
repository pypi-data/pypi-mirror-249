# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import time
import random
from pathlib import Path

import pytest
from rich import print as rprint

from abstract_producer.exc import SendError
from abstract_producer.record import DataClassRecord
from abstract_producer.producer import SimpleProducer
from abstract_producer.logger import logger

dir_here = Path(__file__).absolute().parent


@dataclasses.dataclass
class MySimpleProducer(SimpleProducer):
    def send(self, records: T.List[DataClassRecord]):
        if random.randint(1, 100) <= 50:
            raise SendError("randomly failed due to send error")
        super().send(records)


class TestSimpleProducer:
    @classmethod
    def make_producer(cls) -> MySimpleProducer:
        path_sink = dir_here / "simple_producer_sink.log"
        path_log = dir_here / "simple_producer_buffer.log"
        producer = MySimpleProducer.new(
            backoff_wait_time=[
                1,
                3,
                10,
            ],
            backoff_reset_time=3600,
            path_sink=path_sink,
            path_log=path_log,
            max_buffer_records=5,
        )
        return producer

    def _test_happy_path(self):
        producer = self.make_producer()
        if producer.path.exists():
            producer.path.unlink()
        producer.buffer.clear_persistent()

        # put 1 ~ 12
        for i in range(1, 1 + 12):
            time.sleep(1)
            producer.put(DataClassRecord(id=str(i)), verbose=True)

        records = producer.get_all_records()
        ids = [int(record.id) for record in records]
        assert ids == list(range(1, 1 + 12))

        # put 13 ~ 15
        producer = self.make_producer()
        for i in [13, 14, 15]:
            time.sleep(1)
            producer.put(DataClassRecord(id=str(i)), verbose=True)

        records = producer.get_all_records()
        ids = [int(record.id) for record in records]
        assert ids == list(range(1, 1 + 15))

    def _test_error(self):
        producer = self.make_producer()
        if producer.path.exists():
            producer.path.unlink()
        producer.buffer.clear_persistent()

        with pytest.raises(SendError):
            for i in range(1, 1 + 100):
                time.sleep(0.001)
                producer.put(DataClassRecord(id=str(i)), raise_send_error=True)

    def test(self):
        print("")
        with logger.disabled(
            disable=True,  # no log
            # disable=False, # show log
        ):
            self._test_happy_path()
            self._test_error()


if __name__ == "__main__":
    from abstract_producer.tests import run_cov_test

    run_cov_test(__file__, "abstract_producer.buffer", preview=False)
