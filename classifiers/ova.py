from river import base
from river.multiclass import OneVsRestClassifier
from river.base import Classifier
from ..drift_detectors import NoDrift

class OneVsAllClassifier(OneVsRestClassifier):
    def __init__(self, classifier: Classifier, drift_detector = None):
        super().__init__(classifier)
        if drift_detector == None:
            self.drift_detector = NoDrift()
        else:
            self.drift_detector = drift_detector
        
    
    def learn_one(self, x, y, **kwargs):
        self.drift_detector.update(self.predict_one(x) == y)
        super().learn_one(x, y, **kwargs)
    
    def removeClass(self, y:int):
        self.classifiers.pop(y)