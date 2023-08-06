from typing import Dict, List

from data_classifier.file_handlers.file_handler_base import ABCFileHandler


class FileHandlerComposite(ABCFileHandler):
    def __init__(self, file_handlers: [ABCFileHandler]):
        self.file_handlers = file_handlers

    def get_data_from_file(self, file_path: str) -> Dict[str, List[str]]:
        for file_handler in self.file_handlers:
            if file_handler.validate_file_extension(file_path):
                return file_handler.get_data_from_file(file_path)
        return {}

    def validate_file_extension(self, file_path: str) -> bool:
        return any(file_handler.validate_file_extension(file_path) for file_handler in self.file_handlers)
