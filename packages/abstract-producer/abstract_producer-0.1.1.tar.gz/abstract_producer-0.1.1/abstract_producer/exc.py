# -*- coding: utf-8 -*-


class BufferIsEmptyError(IndexError):
    """
    Raised when try to take item from an empty buffer.
    """
    pass


class SendError(Exception):
    """
    Raised when producer failed to send records.
    """
    pass
