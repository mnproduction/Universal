from datetime import datetime

import os
from datetime import datetime

from handler.fileprocessor import FileProcessor, FileWriter

def test_fileprocessor_initialization(file_processor):
    assert isinstance(file_processor, FileProcessor)

def test_rawprocessor_write(raw_processor: FileWriter, tmp_path):
    content = "test content"
    timestamp = str(datetime.now().strftime('%Y%m%d_%H%M%S'))
    output_folder = str(tmp_path)
    
    # Debugging output
    print(f"Writing to: {output_folder}")
    print(f"Timestamp: {timestamp}")

    raw_processor.write(content, timestamp, output_folder)
    
    expected_filename = f"raw_data_{raw_processor.timestamp}.txt"
    expected_filepath = os.path.join(output_folder, expected_filename)
    
    # Debugging output
    print(f"Expected file path: {expected_filepath}")

    assert os.path.exists(expected_filepath)
    with open(expected_filepath, 'r', encoding='utf-8') as file:
        assert file.read() == content

def test_markdownprocessor_write(markdown_processor: FileWriter, tmp_path):
    content = "# Test Markdown"
    output_folder = str(tmp_path)
    
    markdown_processor.write(content, output_folder)
    
    expected_filename = f"markdown_{markdown_processor.timestamp}.md"
    expected_filepath = os.path.join(output_folder, expected_filename)
    
    assert os.path.exists(expected_filepath)
    with open(expected_filepath, 'r', encoding='utf-8') as file:
        assert file.read() == content

