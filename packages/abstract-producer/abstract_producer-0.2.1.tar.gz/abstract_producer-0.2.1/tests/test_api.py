# -*- coding: utf-8 -*-

from abstract_producer import api


def test():
    _ = api
    _ = api.T_RECORD
    _ = api.T_BUFFER
    _ = api.T_PRODUCER
    _ = api.BaseRecord
    _ = api.DataClassRecord
    _ = api.BaseBuffer
    _ = api.FileBuffer
    _ = api.BaseProducer
    _ = api.SimpleProducer
    _ = api.exc
    _ = api.utils

    _ = api.AwsCloudWatchLogsProducer
    _ = api.KinesisRecord
    _ = api.T_KINESIS_RECORD
    _ = api.KinesisGetRecordsResponseRecord
    _ = api.T_KINESIS_GET_RECORDS_RESPONSE_RECORD
    _ = api.AwsKinesisStreamProducer
    _ = api.Shard
    _ = api.AwsKinesisStreamConsumer


if __name__ == "__main__":
    from abstract_producer.tests import run_cov_test

    run_cov_test(__file__, "abstract_producer.api", preview=False)
