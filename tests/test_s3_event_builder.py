import pytest
from moku.s3 import S3EventBuilder, DefaultS3Event
from moku.s3.exceptions import S3EventException


class TestS3EventBuilder:

    def test_should_build_event_correctly(self):
        event_name = "some.event"
        action = lambda x: print(x)
        event = S3EventBuilder.on(event_name).do(action)
        assert DefaultS3Event(name=event_name, action=action) == event

    def test_should_build_event_directly_with_instance(self):
        event_name = "some.event"
        action = lambda x: print(x)
        event = S3EventBuilder(event_name).do(action)
        assert DefaultS3Event(name=event_name, action=action) == event

    def test_should_raise_exception_when_event_is_not_defined(self):
        with pytest.raises(S3EventException):
            S3EventBuilder().do(lambda x: print(x))
