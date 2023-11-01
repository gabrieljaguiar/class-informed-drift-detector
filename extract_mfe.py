from pymfe.mfe import MFE
from river import tree, drift
from joblib import Parallel, delayed
import itertools
import pandas as pd



from glob import glob
import os
from utils.csv import CSVStream
import warnings
warnings.filterwarnings("ignore")


def task(stream_path,):
    size = 10**6
    window_size = 2500
    stream = CSVStream("{}".format(stream_path))
    stream_name = os.path.splitext(os.path.basename(stream_path))[0]
    stream_output = os.path.dirname(stream_path).replace("datasets", "output")
    print(stream_output)
    exp_name = "{}".format(stream_name)
    print("Running {}...".format(exp_name))
    stream_df_x = []
    stream_df_y = []
    result = []
    
    for i, (x, y) in enumerate(stream):
        stream_df_x.append(x)
        stream_df_y.append(y)   
        if ((i+1)%window_size == 0):
            
            stream_df_x = pd.DataFrame(stream_df_x)
            stream_df_y = pd.DataFrame(stream_df_y)
            stream_df = pd.concat([stream_df_x, stream_df_y], axis=1, ignore_index=True)
            classes = sorted(stream_df.iloc[:, -1].unique())
            for c in classes:
                df = stream_df.loc[stream_df[stream_df.columns[-1]] == c]
                mfe = MFE(groups=["general", "statistical", "info-theory"], summary=["mean"])
                mfe.fit(df.iloc[:, :-1].to_numpy(), df.iloc[:, -1].to_numpy())
                ft = mfe.extract()
                ft = dict(zip(ft[0], ft[1]))
                ft["class_ref"] = c
                ft["idx_ref"] = i
                
                result.append(ft)
            stream_df_x = []
            stream_df_y = []
            #print (ft)
    pd.DataFrame(result).to_csv("{}/{}.csv".format(stream_output,exp_name), index=None)
            
    return result
if __name__ == "__main__":
    PATH = "./datasets/"
    EXT = "*.csv"
    streams = [
        file
        for path, subdir, files in os.walk(PATH)
        for file in glob(os.path.join(path, EXT))
    ]
    
    streams = streams[0:2]
    
    for s in streams:
        task(s)