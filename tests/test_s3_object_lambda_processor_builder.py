import pytest
from moku.s3.object_lambda import ExtensionProcessorBuilder
from moku.s3.object_lambda.exceptions import InvalidExtensionError, InvalidProcessorError


class TestS3ObjectLambdaProcessorBuilder:

    def test_should_create_processor_correctly(self):
        fake_function = lambda x: x
        extension: str = 'jpg'
        processor = ExtensionProcessorBuilder.bind(extension).to(fake_function)

        assert extension == processor.extension
        assert fake_function == processor.func

    def test_should_fail_if_bind_is_not_called(self):

        with pytest.raises(InvalidExtensionError, match='bind'):
            fake_function = lambda x: x
            ExtensionProcessorBuilder().to(fake_function)

    def test_should_raise_an_error_if_func_is_not_callable(self):
        with pytest.raises(InvalidProcessorError, match=r'must be a function or method.'):
            ExtensionProcessorBuilder.bind('ext').to(1)
