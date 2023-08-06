import re

from data_classifier.file_handlers.file_handler_base import ABCFileHandler


class Classifier:
    def __init__(self, file_handler: ABCFileHandler, field_name_keyword: str, field_value_regex: str, field_exclusion_keywords: [str] = None):
        self.file_handler = file_handler
        self.field_name_keyword = field_name_keyword
        self.field_value_regex = field_value_regex
        self.field_exclusion_keywords = field_exclusion_keywords

    def get_keyword(self) -> str:
        return self.field_name_keyword

    def check_field_name(self, field_name: str) -> bool:
        return self.field_name_keyword in field_name.lower()

    def check_field_value(self, field_value: str) -> bool:
        return re.match(self.field_value_regex, field_value) is not None

    def check_for_field_exclusion_keywords(self, field_name: str) -> bool:
        if self.field_exclusion_keywords is None:
            return True
        return not any(keyword in field_name for keyword in self.field_exclusion_keywords)

    def classify(self, file_path: str) -> [str]:
        data_from_file = self.file_handler.get_data_from_file(file_path)
        validated_fields = []
        for field_name, values in data_from_file.items():
            if not self.check_field_name(field_name):
                continue
            if not self.check_for_field_exclusion_keywords(field_name):
                continue
            if any(self.check_field_value(value) for value in values):
                validated_fields.append(field_name)

        return validated_fields
