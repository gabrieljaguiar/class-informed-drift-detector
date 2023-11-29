from river import base
from river.base.classifier import Classifier
from river.naive_bayes.base import BaseNB
from river.naive_bayes.gaussian import GaussianNB
from river import proba
from drift_detectors import MultiDetector
from inspect import isfunction

class AdaGaussianNB(GaussianNB):
    def __init__(self):
        super().__init__()
    def removeClass (self, class_idx):
        #del self.class_counts[class_idx]
        self.gaussians.pop(class_idx)

class AdaNB(base.Classifier):
    def __init__(self, classifier: AdaGaussianNB, drift_detector:  MultiDetector, retrain = False) -> None:
        self.classifier = classifier
        self.drift_detector = drift_detector
        if self.classifier:
            self.nb: base.Classifier = self.classifier
        else:
            self.nb = AdaGaussianNB()
        self.driftDetector = self.drift_detector
        self.retrain = retrain
    
    def learn_one(self, x, y) -> Classifier:
        self.nb.learn_one(x,y)
        self.driftDetector.update(x)
        if (self.driftDetector.drift_detected):
            if (len(self.driftDetector.classes_affected) > 0) and (not self.retrain):
                classes_affected = self.driftDetector.getClassesAffected()
                for c in classes_affected:
                    self.nb.removeClass(c)
            else:
                if self.retrain:
                    self.nb = AdaGaussianNB()
    
    def predict_one(self, x: dict, **kwargs) -> base.typing.ClfTarget | None:
        return self.nb.predict_one(x)
    
    def predict_proba_one(self, x: dict) -> dict[base.typing.ClfTarget, float]:
        return self.nb.predict_proba_one(x)