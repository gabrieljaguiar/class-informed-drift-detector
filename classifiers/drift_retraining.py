from __future__ import annotations

from river import base, drift
from drift_detectors import InformedDrift

class AdaptedDriftRetrainingClassifier(base.Wrapper, base.Classifier):


    def __init__(
        self,
        model: base.Classifier,
        drift_detector: base.DriftAndWarningDetector
        | base.BinaryDriftAndWarningDetector
        | InformedDrift
        | None = None,
        train_in_background: bool = True,
        grace_period = 200,
    ):
        self.model = model
        self.train_in_background = train_in_background
        self.drift_detector = drift_detector if drift_detector is not None else drift.binary.DDM()
        if self.train_in_background:
            self.bkg_model = model.clone()
        self.instance_count = 0
        self.grace_period = grace_period

    @property
    def _wrapped_model(self):
        return self.model

    def predict_proba_one(self, x, **kwargs):
        return self.model.predict_proba_one(x, **kwargs)

    def learn_one(self, x, y, **kwargs):
        self.instance_count += 1
        if self.instance_count > self.grace_period:
            self._update_detector(x, y)
        self.model.learn_one(x, y, **kwargs)
        return self

    def _update_detector(self, x, y):
        
        y_pred = self.model.predict_one(x)
        
        if y_pred is None:
            return

        incorrect_x = 1 if (y == y_pred) else 0
        if type(self.drift_detector) == InformedDrift:
            self.drift_detector.update(x, y)
        else:
            self.drift_detector.update(incorrect_x)
        

        if self.train_in_background:
            if self.drift_detector.warning_detected:
                # If there's a warning, we train the background model
                self.bkg_model.learn_one(x, y)
            elif self.drift_detector.drift_detected:
                # If there's a drift, we replace the model with the background model
                self.model = self.bkg_model
                self.bkg_model = self.model.clone()
        else:
            if type(self.drift_detector) == InformedDrift:
                if self.drift_detector.drift.any():
                    self.model = self.model.clone()
            elif self.drift_detector.drift_detected:
                #print ("{} replace {}".format(self.drift_detector, self.instance_count))
                #print ("{} inside {}".format(self.instance_count, self.drift_detector._p.get()))
                # If there's a drift, we reset the model
                self.model = self.model.clone()

    @classmethod
    def _unit_test_params(cls):
        from river import linear_model, naive_bayes, preprocessing

        yield {
            "model": preprocessing.StandardScaler() | linear_model.LogisticRegression(),
            "drift_detector": drift.binary.DDM(),
        }
        yield {"model": naive_bayes.GaussianNB(), "drift_detector": drift.binary.DDM()}
