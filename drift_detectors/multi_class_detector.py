import numbers
from river.base import DriftDetector
from typing import List

class MultiDetector (DriftDetector):
    def __init__(self):
        super().__init__()
        self.class_affected = []
    
    def getClassesAffected(self):
        return self.classes_affected