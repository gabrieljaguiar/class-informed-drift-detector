# FP = drift alert of a class that did not suffered drift
# TP = drift alert of a class that suffered drift and the alert is a range of -2000, +2000 instances of that class
# FN = no drift alert was raised

from glob import glob
import os
import itertools
import pandas as pd
import numpy as np


def find_closest_drift(drift_list, class_drift_detected, idx):
    available_drift = np.asarray(
        [x for x, y in drift_list if y == class_drift_detected]
    )
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

drift_points = [100000, 200000, 300000]
correct_detections = []

# streams = ["./datasets/swap_cluster_global_gradual_10.csv"]

df_results = []

for stream_path in streams:
    # stream_path = streams[0]

    stream_name = os.path.splitext(os.path.basename(stream_path))[0]

    n_class = int(stream_name.split("_")[-1])
    drift_type = stream_name.split("_")[-2]

    classes_affected = []

    if n_class < 5:
        classes_affected = [n_class - 1]
    else:
        classes_affected = [n_class - 1, n_class - 2]

    drifts_undetected = list(itertools.product(drift_points, classes_affected))
    # print (drifts_undetected)
    drift_alerts = pd.read_csv("../output/backup/alerts_{}.csv".format(stream_name))
    stream_df = pd.read_csv(stream_path)
    # print (drift_alerts)
    tp = 0
    fn = 0
    fp = 0
    avg_delay = 0
    print(stream_name)
    # stream 1 ---- 10000 instances ---- stream 2 10 classes
    # 1000 instances of drifted class
    # 3333 instances of drifted class
    for i, row in drift_alerts.iterrows():
        idx, class_alert = row["idx"], row["class"]
        if class_alert in classes_affected:
            idx_detected = find_closest_drift(drifts_undetected, class_alert, idx)

            if drift_type == "gradual":
                idx_detected -= 5000
            rows = stream_df[
                (stream_df["10"] == class_alert) & (stream_df.index > idx_detected)
            ]
            delay = len(rows[rows.index < idx])
            # filter_df = stream_df[(stream_df.iloc[:, -1:] == class_alert) ]
            # print (filter_df)
            if drift_type == "gradual":
                if delay < 5000 and idx > idx_detected:
                    avg_delay += delay
                    tp += 1
                    idx_detected += 5000
                    drifts_undetected.remove((idx_detected, class_alert))
                    correct_detections.append(
                        {
                            "stream": stream_name,
                            "n_class": n_class,
                            "drift_type": drift_type,
                            "class_affected": abs(n_class-class_alert),
                            "tp": 1,
                            "fp": 0,
                            "fn": 0,
                        }
                    )

                else:
                    fp += 1
            else:
                if delay < 2000 and idx > idx_detected:
                    avg_delay += delay
                    tp += 1
                    drifts_undetected.remove((idx_detected, class_alert))
                    correct_detections.append(
                        {
                            "stream": stream_name,
                            "n_class": n_class,
                            "drift_type": drift_type,
                            "class_affected": abs(n_class-class_alert),
                            "tp": 1,
                            "fp": 0,
                            "fn": 0,
                        }
                    )
                else:
                    fp += 1

        else:
            fp += 1

    fn = len(drifts_undetected)
    for undetected in drifts_undetected:
        correct_detections.append(
            {
                "stream": stream_name,
                "n_class": n_class,
                "drift_type": drift_type,
                "class_affected": abs(n_class-undetected[1]),
                "tp": 0,
                "fp": 0,
                "fn": 1,
            }
        )

    avg_delay += fn * 5000 if drift_type == "gradual" else fn * 1000

    df_results.append(
        {
            "stream": stream_name,
            "n_class": n_class,
            "drift_type": drift_type,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "avg_delay": avg_delay / (tp + fn) if (tp + fn) > 0 else 0,
        }
    )

    del stream_df


pd.DataFrame(df_results).to_csv("results_ciddm_updated.csv", index=None)
pd.DataFrame(correct_detections).to_csv("class_identification_results.csv", index=None)
