from river import base
from river.multiclass import OneVsRestClassifier
from river.base import Classifier

class OneVsAllClassifier(OneVsRestClassifier):
    def __init__(self, classifier: Classifier):
        super().__init__(classifier)
    
    def removeClass(self, y:int):
        self.classifiers.pop(y)