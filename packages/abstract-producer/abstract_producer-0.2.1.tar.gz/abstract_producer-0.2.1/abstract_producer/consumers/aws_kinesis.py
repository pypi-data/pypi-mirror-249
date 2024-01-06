# -*- coding: utf-8 -*-

import time
import typing as T
import dataclasses
from pathlib import Path

from tenacity import retry, wait_exponential, stop_after_attempt, RetryError

from ..vendor.better_dataclass import DataClass
from ..records.aws_kinesis import (
    KinesisGetRecordsResponseRecord,
    T_KINESIS_GET_RECORDS_RESPONSE_RECORD,
)

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager
    from mypy_boto3_kinesis.type_defs import GetRecordsOutputTypeDef


@dataclasses.dataclass
class ShardHashKeyRange(DataClass):
    StartingHashKey: str = dataclasses.field(default=None)
    EndingHashKey: str = dataclasses.field(default=None)


@dataclasses.dataclass
class ShardSequenceNumberRange(DataClass):
    StartingSequenceNumber: str = dataclasses.field(default=None)
    EndingSequenceNumber: str = dataclasses.field(default=None)


@dataclasses.dataclass
class Shard(DataClass):
    # fmt: off
    ShardId: str = dataclasses.field(default=None)
    ParentShardId: T.Optional[str] = dataclasses.field(default=None)
    AdjacentParentShardId: T.Optional[str] = dataclasses.field(default=None)
    HashKeyRange: ShardHashKeyRange = ShardHashKeyRange.nested_field(default_factory=ShardHashKeyRange)
    SequenceNumberRange: ShardSequenceNumberRange = ShardSequenceNumberRange.nested_field(default_factory=ShardSequenceNumberRange)
    # fmt: on

    @classmethod
    def from_list_shards_response(cls, res: dict) -> T.List["Shard"]:
        shards = res.get("Shards", [])
        return [cls.from_dict(shard) for shard in shards]


class ShardIsClosedError(Exception):
    pass


def get_default_backoff_wait_times() -> T.List[int]:
    return [1, 5, 30]


@dataclasses.dataclass
class AwsKinesisStreamConsumer(DataClass):
    """
    User can just call :meth:`Consumer.run` method to start consuming. User also
    can explicitly call :meth:`Consumer.get_records`, :meth:`Consumer.process_record` method
     to get records and process record.
    """

    # fmt: off
    bsm: "BotoSesManager" = dataclasses.field()
    stream_name: str = dataclasses.field()
    shard_id: str = dataclasses.field()
    delay: T.Union[int, float] = dataclasses.field(default=1)
    limit: int = dataclasses.field(default=10000)
    start_shard_iterator: str = dataclasses.field(default=None)
    skip_error: bool = dataclasses.field(default=True)
    backoff_wait_times: T.List[int] = dataclasses.field(default_factory=get_default_backoff_wait_times)

    current_shard_iterator: str = dataclasses.field(init=False)
    next_shard_iterator: T.Optional[str] = dataclasses.field(init=False)
    succeeded_sequence_numbers: T.Set[str] = dataclasses.field(default_factory=set)
    # fmt: on

    def __post_init__(self):
        if self.start_shard_iterator is None:
            self.start_shard_iterator = self.get_checkpoint()
        self.current_shard_iterator = self.start_shard_iterator
        self.next_shard_iterator = None

    @classmethod
    def _get_checkpoint_file(cls, stream_name: str, shard_id: str) -> Path:
        return Path.home().joinpath(
            f".abstract_producer.aws_kinesis.Consumer"
            f".{stream_name}.{shard_id}.checkpoint"
        )

    @property
    def _checkpoint_file(self) -> Path:
        return self._get_checkpoint_file(self.stream_name, self.shard_id)

    def get_checkpoint(self) -> str:
        """
        .. note::

            User could customize this method.
        """
        p = self._checkpoint_file
        if p.exists():
            return p.read_text().strip()
        else:
            res = self.bsm.kinesis_client.get_shard_iterator(
                StreamName=self.stream_name,
                ShardId=self.shard_id,
                ShardIteratorType="LATEST",
            )
            shard_iterator = res["ShardIterator"]
            return shard_iterator

    def set_checkpoint(self):
        """
        This method persist the current shard iterator.

        .. note::

            By default, it will save the checkpoint to ``~/.abstract_producer.aws_kinesis.Consumer.{stream_name}.{shard_id}.checkpoint``.
            In production, you should save it to a more reliable place, such as
            Amazon DynamoDB, Redis.

            User could customize this method.
        """
        self._checkpoint_file.write_text(self.current_shard_iterator)

    def commit(self):
        """
        Commit the current shard iterator.
        """
        if self.next_shard_iterator is None:
            raise ShardIsClosedError
        else:
            self.current_shard_iterator = self.next_shard_iterator
            self.next_shard_iterator = None
            self.set_checkpoint()

    def get_records(
        self,
        limit: T.Optional[int] = None,
    ) -> T.Tuple[
        T.List[T_KINESIS_GET_RECORDS_RESPONSE_RECORD],
        T.Union[dict, "GetRecordsOutputTypeDef"],
    ]:
        """
        Call ``boto3.client("kinesis").get_records(...)`` API to get records.
        """
        if limit is None:
            limit = self.limit
        res = self.bsm.kinesis_client.get_records(
            ShardIterator=self.current_shard_iterator,
            Limit=limit,
        )
        self.next_shard_iterator = res.get("NextShardIterator")
        records = KinesisGetRecordsResponseRecord.from_get_records_response(res)
        return records, res

    def user_process_record(
        self,
        record: T_KINESIS_GET_RECORDS_RESPONSE_RECORD,
    ):
        """
        This method defines how to process a failed record.

        .. important::

            User has to implement this method.
        """
        raise NotImplementedError

    def user_process_failed_record(
        self,
        record: T_KINESIS_GET_RECORDS_RESPONSE_RECORD,
    ):
        """
        This method defines how to process a failed record.

        .. note::

            By default, it does nothing. In production, you should send
            this record to a dead-letter-queue (DLQ) for further investigation.

            User could customize this method.
        """
        return record

    # todo: allow user to customize exponential backoff wait times
    @retry(
        wait=wait_exponential(multiplier=1, exp_base=2, min=0, max=30),
        stop=stop_after_attempt(4),
    )
    def _process_record(
        self,
        record: T_KINESIS_GET_RECORDS_RESPONSE_RECORD,
    ) -> T.Tuple[bool, T.Any]:
        """
        Add retry mechanism to ``self.user_process_record``.
        """
        return self.user_process_record(record)

    def process_record(
        self,
        record: T_KINESIS_GET_RECORDS_RESPONSE_RECORD,
    ) -> T.Tuple[bool, T.Any]:
        """
        This is the internal implementation of ``process_record`` method.
        It is a wrapper of user's ``process_record`` method, and provide
        retry, checkpoint, and error handling features.

        """
        try:
            res = self._process_record(record)
            return True, res
        except RetryError as e:
            res = self.user_process_failed_record(record)
            if self.skip_error:
                return False, res
            else:
                e.reraise()

    def run(self):
        """
        Run the consumer.
        """
        while 1:
            records, get_records_res = self.get_records()
            for record in records:
                flag, process_record_res = self.process_record(record)
            self.commit()
            time.sleep(self.delay)
