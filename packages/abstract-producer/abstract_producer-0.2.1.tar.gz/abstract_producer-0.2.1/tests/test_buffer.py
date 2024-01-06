# -*- coding: utf-8 -*-

import pytest

import time
from pathlib import Path

from abstract_producer.record import DataClassRecord
from abstract_producer.buffer import FileBuffer, BufferIsEmptyError
from rich import print as rprint

dir_here = Path(__file__).absolute().parent


class TestFileBuffer:
    path_log = dir_here.joinpath("file_buffer.log")

    def _test_happy_path(self):
        buffer = FileBuffer.new(
            record_class=DataClassRecord,
            path=self.path_log,
            max_records=2,
            max_size=1000000,
        )
        buffer.clear_persistent()  # reset everything
        assert len(buffer._mem_queue) == 0
        assert len(buffer._mem_serialized_queue) == 0
        assert len(buffer._file_queue) == 0
        assert buffer.path.exists() is False

        # put records 1, 2, 3
        record_list = [DataClassRecord(id=str(i)) for i in [1, 2, 3]]
        emitted_records_list = list()
        for record in record_list:
            time.sleep(0.001)
            buffer.put(record)
            if buffer.should_i_emit():
                emitted_records = buffer.emit()
                emitted_records_list.append(emitted_records)
                buffer.task_done()
        # rprint(record_list)
        # rprint(emitted_records_list)

        assert len(emitted_records_list) == 1
        for emitted_records in emitted_records_list:
            assert len(emitted_records) == 2
        assert emitted_records_list[0][0].id == "1"
        assert emitted_records_list[0][1].id == "2"
        assert buffer.path.exists() is True

        # put records 4, 5, but not emit anything
        record_list = [DataClassRecord(id=str(i)) for i in [4, 5]]
        for record in record_list:
            time.sleep(0.001)
            buffer.put(record)

        assert len(buffer._file_queue) == 1

        print("-" * 80)
        # recover the buffer from persistence
        buffer = FileBuffer.new(
            record_class=DataClassRecord,
            path=self.path_log,
            max_records=2,
            max_size=1000000,
        )
        assert len(buffer._mem_queue) == 1
        assert len(buffer._file_queue) == 1
        assert buffer.queue[0].id == "5"

        # put records 6, 7, 8, 9
        new_record_list = [DataClassRecord(id=str(i)) for i in [6, 7, 8, 9]]
        emitted_records_list = list()
        for record in new_record_list:
            time.sleep(0.001)
            buffer.put(record)
            if buffer.should_i_emit():
                emitted_records = buffer.emit()
                emitted_records_list.append(emitted_records)
                buffer.task_done()
        # rprint(new_record_list)
        # rprint(emitted_records_list)

        assert len(emitted_records_list) == 3
        for emitted_records in emitted_records_list:
            assert len(emitted_records) == 2
        assert emitted_records_list[0][0].id == "3"
        assert emitted_records_list[0][1].id == "4"
        assert emitted_records_list[1][0].id == "5"
        assert emitted_records_list[1][1].id == "6"
        assert emitted_records_list[2][0].id == "7"
        assert emitted_records_list[2][1].id == "8"

        assert buffer.path.exists() is True

        emitted_records = buffer.emit()
        buffer.task_done()
        assert len(emitted_records) == 1
        assert emitted_records[0].id == "9"
        assert buffer.path.exists() is False

        with pytest.raises(BufferIsEmptyError):
            buffer.emit()

        with pytest.raises(BufferIsEmptyError):
            buffer.task_done()

    def test(self):
        print("")
        self._test_happy_path()


if __name__ == "__main__":
    from abstract_producer.tests import run_cov_test

    run_cov_test(__file__, "abstract_producer.buffer", preview=False)
