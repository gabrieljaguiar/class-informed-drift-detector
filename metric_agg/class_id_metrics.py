from glob import glob
import os
import itertools
import pandas as pd
import numpy as np

dd_data = pd.read_csv("./class_identification_results.csv")

dd_data.drop(["stream","drift_type", "fp"], axis = 1, inplace=True)

#stream,n_class,drift_type,class_affected,tp,fp,fn

agg = dd_data.groupby(["n_class", "class_affected"]).sum().reset_index()

print(agg.groupby("n_class")[["tp", "fp"]].transform(lambda x: x/x.sum()))

agg.to_csv("agg_class_id_results.csv", index=None)