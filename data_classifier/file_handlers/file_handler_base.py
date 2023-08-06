from abc import abstractmethod
from typing import Dict, List


class ABCFileHandler:
    @abstractmethod
    def get_data_from_file(self, file_path: str) -> Dict[str, List[str]]:
        pass

    @abstractmethod
    def validate_file_extension(self, file_path: str) -> bool:
        pass
