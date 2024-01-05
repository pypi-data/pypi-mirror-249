
.. image:: https://readthedocs.org/projects/abstract-producer/badge/?version=latest
    :target: https://abstract-producer.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/abstract_producer-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/abstract_producer-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/abstract_producer-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/abstract_producer-project

.. image:: https://img.shields.io/pypi/v/abstract-producer.svg
    :target: https://pypi.python.org/pypi/abstract-producer

.. image:: https://img.shields.io/pypi/l/abstract-producer.svg
    :target: https://pypi.python.org/pypi/abstract-producer

.. image:: https://img.shields.io/pypi/pyversions/abstract-producer.svg
    :target: https://pypi.python.org/pypi/abstract-producer

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/abstract_producer-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/abstract_producer-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://abstract-producer.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://abstract-producer.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/abstract_producer-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/abstract_producer-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/abstract_producer-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/abstract-producer#files


Welcome to ``abstract_producer`` Documentation
==============================================================================
📔 See `Full Documentation HERE <https://abstract-producer.readthedocs.io/>`_.

.. image:: https://github.com/MacHu-GWU/abstract_producer-project/assets/6800411/0bbfba0c-12e4-413c-bfea-d68a1ead4369

This library provides the abstraction of data producer, which is a common client sending data to stream processing system, such as Apache Kafka, Apache Pulsar, AWS Kinesis, AWS SQS, AWS CloudWatch logs, etc.

It has the following business critical features out-of-box:

1. group records into micro batch to maximize the utilization of network bandwidth.
2. use local write-ahead-log to prevent unexpected error and data loss.
3. auto-retry using exponential backoff strategy to handle transient error.

With this library, it is easy to create data producer client library for any stream processing system.


Usage Examples
------------------------------------------------------------------------------
- `A POC producer <https://github.com/MacHu-GWU/abstract_producer-project/blob/main/examples/simple_producer.py>`_ This is a very simple producer that write data to a local, append-only file.
- `AWS CloudWatch Logs producer <https://github.com/MacHu-GWU/abstract_producer-project/blob/main/examples/aws_cloudwatch_logs_producer.py>`_.


.. _install:

Install
------------------------------------------------------------------------------

``abstract_producer`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install abstract-producer

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade abstract-producer
