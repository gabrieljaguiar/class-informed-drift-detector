from river import base
from river.base.classifier import Classifier
from river.naive_bayes.base import BaseNB
from river.naive_bayes.gaussian import GaussianNB
from river import proba
from drift_detectors import MultiDetector

class AdaGaussianNB(GaussianNB):
    def __init__(self):
        super().__init__()
    def removeClass (self, class_idx):
        self.class_counts[class_idx] = 0
        for i in self.gaussians[class_idx]:
            self.gaussians[class_idx][i] = proba.Gaussian

class AdaNB(base.Classifier):
    def __init__(self, classifier: AdaGaussianNB, drift_detector:  MultiDetector) -> None:
        if classifier:
            self.nb: base.Classifier = classifier
        else:
            self.nb = AdaGaussianNB()
        self.driftDetector = drift_detector
    
    def learn_one(self, x, y) -> Classifier:
        self.nb.learn_one(x,y)
        self.driftDetector.update(x)
        if (self.driftDetector.drift_detected):
            if type (self.drift_detector) == MultiDetector:
                classes_affected = self.driftDetector.getClassesAffected()
                for c in classes_affected:
                    self.nb.removeClass(c)
            else:
                self.nb = AdaGaussianNB()
    
    def predict_one(self, x: dict, **kwargs) -> base.typing.ClfTarget | None:
        return self.nb.predict_one(x)
    
    def predict_proba_one(self, x: dict) -> dict[base.typing.ClfTarget, float]:
        return self.nb.predict_proba_one(x)