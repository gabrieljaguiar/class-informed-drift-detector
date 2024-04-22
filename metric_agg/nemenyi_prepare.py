from glob import glob
import pandas as pd
import numpy as np

dd_data = pd.read_csv("./results_dd.csv")
dd_data_ciddm = pd.read_csv("./results_ciddm_updated.csv")
dd_data_ciddm["classif"] = "NB"
dd_data_ciddm["dd"] = "CIDDM"
dd_data = pd.concat([dd_data, dd_data_ciddm], axis=0)

dd_data = dd_data[dd_data["classif"]== "NB"]

dd_data = dd_data[dd_data["n_class"] < 20]

dd_data.drop(["classif", "n_class"], inplace=True, axis=1)
#sum_df = dd_data.groupby(["n_class", "drift_type", "classif", "dd"]).sum()
#avg_df = dd_data.groupby(["n_class", "drift_type", "classif", "dd"]).mean()

final_df = dd_data
final_df["precision"] = final_df["tp"]/(final_df["tp"]+final_df["fp"]) #if (final_df["tp"]+final_df["fp"]) > 0 else 0
final_df["precision"].fillna(0, inplace=True)
final_df["recall"] = final_df["tp"]/(final_df["tp"]+final_df["fn"]) #if (dd_data["tp"]+dd_data["fn"]) > 0 else 0
final_df["recall"].fillna(0, inplace=True)
final_df["f1"] = 2*final_df["precision"]*final_df["recall"]/(final_df["precision"]+final_df["recall"])
final_df["f1"].fillna(0, inplace=True)

final_df.drop(["precision", "recall", "drift_type", "tp", "fp", "fn", "avg_delay"], inplace=True, axis=1)

table = final_df.pivot(index="stream", values="f1", columns=["dd"]).reset_index()

table.drop(["stream"], axis=1).to_csv("nemenyi_nb.csv", index=None)