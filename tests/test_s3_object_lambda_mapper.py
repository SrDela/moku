import pytest
from moku.s3.object_lambda import ExtensionMapper, ExtensionProcessorBuilder
from moku.s3.object_lambda.exceptions import InvalidExtensionError


class TestS3ObjectLambdaMapper:

    def test_should_add_extensions_and_resolve_correctly(self):
        extension = 'jpg'
        other_extension = 'png'
        processor = ExtensionProcessorBuilder.bind(extension).to(lambda x: x)
        other_processor = ExtensionProcessorBuilder.bind(other_extension).to(lambda y: y)

        mapper = ExtensionMapper()
        mapper.add_extension(processor)
        mapper.add_extension(other_processor)

        result = mapper.resolve(extension)
        assert processor.func == result

        result = mapper.resolve(other_extension)
        assert other_processor.func == result

    def test_should_fail_if_extension_is_not_mapped(self):
        processor = ExtensionProcessorBuilder.bind('jpg').to(lambda x: x)

        mapper = ExtensionMapper()
        mapper.add_extension(processor)

        with pytest.raises(InvalidExtensionError, match='is not mapped'):
            mapper.resolve('png')

    def test_should_fail_if_extension_is_already_mapped(self):
        processor = ExtensionProcessorBuilder.bind('jpg').to(lambda x: x)
        other_processor = ExtensionProcessorBuilder.bind('jpg').to(lambda y: y)

        mapper = ExtensionMapper()
        with pytest.raises(InvalidExtensionError, match='Already mapped'):
            mapper.add_extension(processor)
            mapper.add_extension(other_processor)
