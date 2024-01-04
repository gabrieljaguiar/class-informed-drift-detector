from river.base import DriftDetector
import numpy as np
from sklearn.svm import OneClassSVM
import collections
from pymfe.mfe import MFE
import pandas as pd


class MultiDetector(DriftDetector):
    def __init__(self):
        super().__init__()
        self.class_affected = []

    def getClassesAffected(self):
        return self.classes_affected


class InformedDrift(MultiDetector):
    def __init__(
        self, n_classes: int, window_size: int = 100, windows_to_train: int = 10
    ):
        super().__init__()
        self.classifiers = {}
        self.windows = {
            key: collections.deque(maxlen=window_size) for key in range(0, n_classes)
        }
        self.current_concept = {key: [] for key in range(0, n_classes)}
        self.window_size = window_size
        self.windows_to_train = windows_to_train

    def update(self, x: np.array, y: int):
        x["class"] = y
        self.windows[y].append(x)
        if len(self.windows[y]) == self.windows[y].maxlen:
            #print (len(self.windows[y]))
            df = pd.DataFrame(self.windows[y])
            mfe = MFE(groups=["general", "statistical"], summary=["mean"])
            mfe.fit(df.iloc[:, :-1].to_numpy(), df.iloc[:, -1].to_numpy())
            ft = mfe.extract()
            ft = dict(zip(ft[0], ft[1]))
            self.current_concept[y].append(ft)
            self.windows[y].clear()
            #print (self.current_concept[y])
            # extract features
            # predict if there is a drift in that class or not
            # if not add this features to the current concept of that class
            # if drift detected  raise drift alarm, classes affected == y, reset one class classifier plus reset current concept
            #pass
            if (self.classifiers.get(y, None)):
                array_to_predict = np.array(list(self.current_concept[y][-1].values()))
                array_to_predict = array_to_predict[~np.isnan(array_to_predict)].reshape(1,-1)
                #print (array_to_predict)
                print(self.classifiers[y].predict(array_to_predict))
            if (len(self.current_concept[y]) > self.windows_to_train): #and (self.classifiers.get(y, None) == None):
                self.classifiers[y] = OneClassSVM()
                df = pd.DataFrame(self.current_concept[y]).dropna(axis=1, inplace=False)
                self.classifiers[y].fit(df)
                del df
        
        self._drift_detected = False