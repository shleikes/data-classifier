from data_classifier.classifiers.classifier import Classifier


class ClassifierRunner:
    def __init__(self, classifiers: [Classifier]):
        self.classifiers = classifiers

    def run_classifiers(self, file_path: str) -> [dict]:
        ret = []
        for classifier in self.classifiers:
            fields = classifier.classify(file_path)
            ret.append({
                "data_classifier": classifier.get_keyword(),
                "fields": fields
            })
        return ret
