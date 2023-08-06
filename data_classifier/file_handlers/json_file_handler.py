import os
import json
from typing import Dict, List

from data_classifier.file_handlers.file_handler_base import ABCFileHandler


class JsonFileHandler(ABCFileHandler):
    def get_data_from_file(self, file_path: str) -> Dict[str, List[str]]:
        if not self.validate_file_extension(file_path):
            raise ValueError(f"File {file_path} is not a JSON file")

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        with open(file_path, "r") as file:
            json_reader = json.load(file)
            if json_reader is None:
                raise ValueError(f"File {file_path} is empty")

            return self.get_paths(json_reader)

    def validate_file_extension(self, file_path: str) -> bool:
        return file_path.endswith(".json")

    @staticmethod
    def add_if_not_exists(paths, current_path, value) -> Dict[str, List[str]]:
        path = current_path[:-1]
        if path not in paths:
            paths[path] = []
        paths[path].append(value)
        return paths

    def get_paths(self, obj, current_path=None, paths=None) -> Dict[str, List[str]]:
        if paths is None:
            paths = {}
        if current_path is None:
            current_path = ""

        if isinstance(obj, list):
            for child in obj:
                current_path += "[]."
                return {**paths, **self.get_paths(child, current_path, paths)}
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    paths = {**paths, **self.get_paths(v, current_path + f"{k}.", paths)}
                elif isinstance(v, list):
                    for idx, item in enumerate(v):
                        paths = {**paths, **self.get_paths(item, current_path + f"{k}.[].", paths)}
                else:
                    paths = self.add_if_not_exists(paths, current_path + f"{k}.", v)
        else:
            paths = self.add_if_not_exists(paths, current_path, obj)
        return paths

