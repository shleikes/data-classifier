import sys

from data_classifier.classifiers.classifier import Classifier
from data_classifier.classifiers.classifier_runner import ClassifierRunner
from data_classifier.file_handlers.file_handler_composite import FileHandlerComposite
from data_classifier.file_handlers.json_file_handler import JsonFileHandler
from data_classifier.file_handlers.csv_file_handler import CSVFileHandler


def classify(file_path: str):
    if not file_path:
        raise ValueError("File path is empty")

    file_handler_composite = FileHandlerComposite([
        CSVFileHandler(),
        JsonFileHandler()
    ])

    classifier_runner = ClassifierRunner(classifiers=[
        Classifier(file_handler_composite, "email",
                   r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"),
        Classifier(file_handler_composite, "phone",
                   r"^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4}$",
                   ["serialNumber"]),
    ])

    for classifier_data in classifier_runner.run_classifiers(file_path):
        print(classifier_data["fields"], classifier_data["data_classifier"])


if __name__ == '__main__':
    sys.exit(classify(sys.argv[1]))
