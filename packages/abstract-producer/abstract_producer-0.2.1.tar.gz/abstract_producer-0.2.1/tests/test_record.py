# -*- coding: utf-8 -*-

from datetime import datetime
from abstract_producer.record import DataClassRecord


class TestDataClassRecord:
    def test(self):
        r = DataClassRecord()
        assert isinstance(r.create_at_dt, datetime)
        assert r.create_at_dt.tzinfo is not None
        r1 = DataClassRecord.deserialize(r.serialize())
        assert r == r1


if __name__ == "__main__":
    from abstract_producer.tests import run_cov_test

    run_cov_test(__file__, "abstract_producer.record", preview=False)
