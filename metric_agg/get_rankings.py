from glob import glob
import os
import itertools
import pandas as pd
import numpy as np

dd_data = pd.read_csv("./results_dd.csv")
dd_data_ciddm = pd.read_csv("./results_ciddm.csv")
dd_data_ciddm["classif"] = "HT"
dd_data_ciddm["dd"] = "CIDDM"
dd_data = pd.concat([dd_data, dd_data_ciddm], axis=0)

dd_data = dd_data[dd_data["classif"]== "HT"]

dd_data = dd_data[dd_data["n_class"] < 20]

dd_data["precision"] = dd_data["tp"]/(dd_data["tp"]+dd_data["fp"]) #if (dd_data["tp"]+dd_data["fp"]) > 0 else 0
dd_data["precision"].fillna(0, inplace=True)
dd_data["recall"] = dd_data["tp"]/(dd_data["tp"]+dd_data["fn"]) #if (dd_data["tp"]+dd_data["fn"]) > 0 else 0
dd_data["recall"].fillna(0, inplace=True)

dd_data["f1"] = 2*dd_data["precision"]*dd_data["recall"]/(dd_data["precision"]+dd_data["recall"])
dd_data["f1"].fillna(0, inplace=True)


rank = dd_data[["stream", "precision", "f1"]].groupby("stream").rank("average", ascending=False)
rank["delay"] =  dd_data[["stream", "avg_delay"]].groupby("stream").rank("average")

rank["dd"] = dd_data["dd"]
rank.groupby(["dd"]).mean().to_csv("ranking_total_ht.csv")

rank["n_class"] =dd_data["n_class"]
rank["drift_type"] =dd_data["drift_type"]
#ranking = ht_data.groupby(["stream"]).rank("average")

#ranking["stream"] = ht_data["stream"]
#ranking["dd_name"] = ht_data["dd"]



rank.groupby(["dd","n_class","drift_type"]).mean().to_csv("ranking_average_ht.csv")

rank["stream"] = dd_data["stream"]
rank.sort_values(by="stream", inplace=True)
rank.to_csv("ranking_ht.csv", index=None)