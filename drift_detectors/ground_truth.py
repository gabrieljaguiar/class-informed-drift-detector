import numbers
from river.base import DriftDetector
from typing import List

class TruthDetector (DriftDetector):
    def __init__(self, drift_point: int, classes_affected: List):
        super().__init__()
        self.drift_point = drift_point
        self.instanceCount = 0
        self.classes_affected = classes_affected
    def update(self, x) -> DriftDetector:
        self.instanceCount += 1
        if self.instanceCount == self.drift_point:
            self._drift_detected = True
        else:
            self._drift_detected = False
    
    def getClassesAffected(self):
        return self.classes_affected