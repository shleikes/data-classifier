import csv
import os
from typing import Dict, List

from data_classifier.file_handlers.file_handler_base import ABCFileHandler


class CSVFileHandler(ABCFileHandler):
    def get_data_from_file(self, file_path: str) -> Dict[str, List[str]]:
        if not self.validate_file_extension(file_path):
            raise ValueError(f"File {file_path} is not a CSV file")

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        with open(file_path, "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            columns = next(csv_reader)
            data = {key: [] for key in columns}
            for row in csv_reader:
                for idx, cell in enumerate(row):
                    data[columns[idx]].append(cell)

            return data

    def validate_file_extension(self, file_path: str) -> bool:
        return file_path.endswith(".csv")
