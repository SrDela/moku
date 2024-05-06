import pytest
from typing import Callable
from moku.s3 import S3EventMapper, S3EventBuilder, DefaultS3Event
from moku.s3.exceptions import S3EventException


class TestS3EventMapper:

    func: Callable[[any], any] = lambda x: x
    func2: Callable[[any], str] = lambda x: str(x)

    def test_should_add_event_and_resolve_correctly(self):
        event_name: str = "fake.event"
        event: DefaultS3Event = S3EventBuilder.on(event_name).do(self.func)
        mapper = S3EventMapper()
        mapper.add_event(event)
        action = mapper.resolve(event_name)

        assert self.func == action

    def test_should_overwrite_event_and_resolve_correctly(self):
        event_name: str = "fake.event"
        event: DefaultS3Event = S3EventBuilder.on(event_name).do(self.func)
        event2: DefaultS3Event = S3EventBuilder.on(event_name).do(self.func2)
        mapper = S3EventMapper()
        mapper.add_event(event)
        mapper.add_event(event2)
        action = mapper.resolve(event_name)

        assert self.func2 == action

    def test_should_raise_error_if_event_is_not_mapped(self):
        event_name: str = "fake.event"
        event: DefaultS3Event = S3EventBuilder.on(event_name).do(self.func)
        mapper = S3EventMapper()
        mapper.add_event(event)

        with pytest.raises(S3EventException):
            mapper.resolve("other.event")
