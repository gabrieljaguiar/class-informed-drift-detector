from glob import glob
import os
import pandas as pd
    

clfs = ["ADWIN",
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
    "CIDDM",
    "NO_DRIFT",
    "GT"
]
classes =[2,3,5, 10]
classes_affected = [[2], [2,3], [2,3,5], [2, 5, 10]]

PATH = "../output/"

df_results = []

for clf in clfs:
    for cn in classes:
        c_aff = classes_affected [classes.index(cn)]
        for ca in c_aff:
            EXT = "NB_RT_{}_ground_truth_multi_class_global_*_ds_1_c_{}_ca_{}_*.csv".format(clf, cn, ca)
            result_csv = [
                file
                for path, subdir, files in os.walk(PATH)
                for file in glob(os.path.join(path, EXT))
            ]

            for res in result_csv:
                df_row = {}
                df_row["clf"] = clf
                df_row["n_classes"] = cn
                df_row["c_affected"] = ca
                df = pd.read_csv(res)
                df_row["accuracy"] = df["accuracy"].mean()
                df_row["drift_accuracy"] = df["accuracy"].iloc[99:101].mean()
                mean_affected = 0
                for i in range(cn - ca, cn):
                    mean_affected += df["class_{}".format(i)].mean()
                
                mean_affected = mean_affected/ (ca)
                df_row["mean_gmean_aff"] = mean_affected
            
                df_results.append(df_row)

pd.DataFrame(df_results).to_csv("nb_agg_metrics.csv", index=None)