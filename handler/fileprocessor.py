# handler/fileprocessor.py

import json
import os
from datetime import datetime
from abc import ABC, abstractmethod

import pandas as pd


class FileProcessor(ABC):
    pass

class FileWriter(FileProcessor):
    @abstractmethod
    def write(self):
        pass

class FileLoader(FileProcessor):
    @abstractmethod
    def load(self) -> str:
        pass



class RawProcessor(FileWriter):
    def __init__(self, file_path: str = "./output/raw_data"):
        self.file_path = file_path
        self.timestamp = datetime.now()

    def write(self, content: str, timestamp: datetime | None = None, output_folder: str = "./output/raw_data"):
        os.makedirs(output_folder, exist_ok=True)
        if not timestamp:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_folder, f"raw_data_{timestamp}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

class MarkdownProcessor(FileWriter):
    def __init__(self, file_path: str = "./output/markdown"):
        self.file_path = file_path
        self.timestamp = datetime.now()

    def write(self, content: str, timestamp: datetime | None = None, output_folder: str = "./output/markdown"):
        os.makedirs(output_folder, exist_ok=True)
        if not timestamp:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_folder, f"markdown_{timestamp}.md")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

class JsonProcessor(FileWriter):
    def __init__(self, file_path: str = "./output/json"):
        self.file_path = file_path
        self.timestamp = datetime.now()

    def write(self, content: str, timestamp: datetime | None = None, output_folder: str = "./output/formatted_data"):
        formatted_data_dict = content.dict() if hasattr(content, 'dict') else content

        os.makedirs(output_folder, exist_ok=True)
        if not timestamp:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")    
        file_path = os.path.join(output_folder, f"formatted_data_{timestamp}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(formatted_data_dict, file, indent=4)

class ExcelProcessor(FileWriter):
    def __init__(self, file_path: str = "./output/excel"):
        self.file_path = file_path
        self.timestamp = datetime.now()

    def write(self, content: pd.DataFrame, timestamp: datetime | None = None, output_folder: str = "./output/excel"):
        os.makedirs(output_folder, exist_ok=True)
        if not timestamp:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")    
        file_path = os.path.join(output_folder, f"sorted_data_{timestamp}.xlsx")
        content.to_excel(file_path, index=False)



