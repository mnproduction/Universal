import pytest
from handler.fileprocessor import FileProcessor, RawProcessor, MarkdownProcessor

@pytest.fixture
def file_processor():
    return FileProcessor()

@pytest.fixture
def raw_processor():
    return RawProcessor()

@pytest.fixture
def markdown_processor():
    return MarkdownProcessor()