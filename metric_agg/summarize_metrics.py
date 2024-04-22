# FP = drift alert of a class that did not suffered drift
# TP = drift alert of a class that suffered drift and the alert is a range of -2000, +2000 instances of that class
# FN = no drift alert was raised 

from glob import glob
import os
import itertools
import pandas as pd
import numpy as np


def find_closest_drift (drift_list,  idx):
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



#streams = ["../datasets/prune_growth_new_branch_local_gradual_5.csv"]

df_results = []

drift_detectors = [
    "CIDDM",
    "NO_DRIFT",
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
    "GT"]

classifiers = ["HT_RT"]


for c in classifiers:
    for dd in drift_detectors:
        for stream_path in streams:
            
            stream_name = os.path.splitext(os.path.basename(stream_path))[0]

            n_class = int(stream_name.split("_")[-1])
            drift_type = stream_name.split("_")[-2]

        
            #print (drifts_undetected)
            metrics = pd.read_csv("../output/{}_{}_{}.csv".format(c, dd,stream_name))
            #,idx,accuracy,gmean,kappa,class_0,class_prop_0,class_1,class_prop_1,class_2,class_prop_2,class_3,class_prop_3,class_4,class_prop_4,drifts_alerts,local_alerts
            
            acc_mean = metrics["accuracy"].mean()
            gmean_mean = metrics["gmean"].mean()
            kappa_mean = metrics["kappa"].mean()
            
            affected_class_1 = metrics["class_{}".format(n_class - 1)].mean()
            affected_class_2 = metrics["class_{}".format(n_class - 2)].mean()
            
            if n_class == 3:
                affected_class_2 = affected_class_1
            

            df_results.append({
                    "stream": stream_name,
                    "n_class": n_class,
                    "drift_type": drift_type,
                    "classif": c,
                    "dd": dd,
                    "acc": acc_mean,
                    "gmean": gmean_mean,
                    "kappa": kappa_mean,
                    "aff_c1": affected_class_1,
                    "aff_c2":affected_class_2

                })


df_results = pd.DataFrame(df_results)

avg_df = df_results.drop(["stream", "classif"], axis=1).groupby(["n_class", "drift_type", "dd"]).mean()

avg_df["acc_rank"] = avg_df.groupby(["n_class", "drift_type"])["acc"].rank(ascending=False)
avg_df["gmean_rank"] = avg_df.groupby(["n_class", "drift_type"])["gmean"].rank(ascending=False)
avg_df["c1_rank"] = avg_df.groupby(["n_class", "drift_type"])["aff_c1"].rank(ascending=False)
avg_df = avg_df.reset_index()
rank_df = avg_df[["dd", "acc_rank", "gmean_rank"]]
rank_df.groupby("dd").mean().reset_index().to_csv("rank_metrics_ht.csv")


avg_df.to_csv("results_metrics_ht_agg.csv", index=None)

#rank.to_csv("results_metrics_ht_rank.csv", index=None)
#pd.DataFrame(df_results).to_csv("results_metrics_ht.csv", index=None)