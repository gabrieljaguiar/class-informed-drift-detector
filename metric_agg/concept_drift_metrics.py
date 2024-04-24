# FP = drift alert of a class that did not suffered drift
# TP = drift alert of a class that suffered drift and the alert is a range of -2000, +2000 instances of that class
# FN = no drift alert was raised

from glob import glob
import os
import itertools
import pandas as pd
import numpy as np


def find_closest_drift(drift_list, idx):
    available_drift = drift_list
    if len(available_drift) == 0:
        return None
    closest = (np.abs(available_drift - idx)).argmin()
    return available_drift[closest]


PATH = "../datasets/"
EXT = "*.csv"
streams = [
    file
    for path, subdir, files in os.walk(PATH)
    for file in glob(os.path.join(path, EXT))
]

streams = sorted(streams)


# streams = ["../datasets/prune_growth_new_branch_local_gradual_5.csv"]

df_results = []

drift_detectors = [
    "ADWIN",
    "PageHinkley",
    "HDDM",
    "KSWIN",
    "DDM",
    "RDDM",
    "STEPD",
    "ECDD",
    "EDDM",
    "FHDDM",
    "FHDDMS",
]

classifiers = ["HT", "NB"]


for c in classifiers:
    for dd in drift_detectors:
        for stream_path in streams:

            stream_name = os.path.splitext(os.path.basename(stream_path))[0]

            n_class = int(stream_name.split("_")[-1])
            drift_type = stream_name.split("_")[-2]

            drift_points = [100000, 200000, 300000]
            drifts_undetected = drift_points
            # print (drifts_undetected)
            drift_alerts = pd.read_csv(
                "../output/backup/drift_alerts_{}_{}_{}.csv".format(c, dd, stream_name)
            )
            # print (drift_alerts)

            # print (drift_alerts)
            tp = 0
            fn = 0
            fp = 0
            avg_delay = 0
            print(stream_name)

            # print (drift_alerts)
            for _, row in drift_alerts.iterrows():
                idx = row["idx"]

                idx_detected = find_closest_drift(drifts_undetected, idx)

                if idx_detected == None:
                    fp += 1
                else:
                    if drift_type == "gradual":
                        idx_detected -= 5000

                    delay = abs(idx_detected - idx)
                    if drift_type == "gradual":
                        if delay < 10000 and idx > idx_detected:
                            avg_delay += delay
                            tp += 1
                            idx_detected += 5000
                            drifts_undetected.remove(idx_detected)
                        else:
                            fp += 1
                    else:
                        if delay < 2000 and idx > idx_detected:
                            avg_delay += delay
                            tp += 1
                            drifts_undetected.remove(idx_detected)
                        else:
                            fp += 1

            fn = len(drifts_undetected)
            avg_delay += fn * 10000 if drift_type == "gradual" else fn * 2000

            df_results.append(
                {
                    "stream": stream_name,
                    "n_class": n_class,
                    "drift_type": drift_type,
                    "classif": c,
                    "dd": dd,
                    "tp": tp,
                    "fp": fp,
                    "fn": fn,
                    "avg_delay": avg_delay / (tp + fn) if (tp + fn) > 0 else 0,
                }
            )


pd.DataFrame(df_results).to_csv("results_dd_update.csv", index=None)
