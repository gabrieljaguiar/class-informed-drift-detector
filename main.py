from river import tree, drift
from experiment import Experiment
from joblib import Parallel, delayed
import itertools
from glob import glob
import os
from utils.csv import CSVStream
from drift_detectors import NoDrift, TruthDetector
from classifiers import AdaNB

models = [
    ("NB", AdaNB(classifier=None, drift_detector=NoDrift()))
]

dds = [
    ("No_drift", NoDrift()),
    ("ground_truth", TruthDetector(50000, classes_affected=[9,8,7,6,5]))
]


def task(stream_path, model, dd):
    stream = CSVStream("{}".format(stream_path))
    stream_name = os.path.splitext(os.path.basename(stream_path))[0]
    stream_output = "./output/"
    print(stream_output)
    model_name, model = model
    dd_name, dd = dd
    exp_name = "{}_{}_{}".format(model_name, dd_name, stream_name)
    print("Running {}...".format(exp_name))
    exp = Experiment(exp_name, stream_output, model, dd, stream, stream_size=100000)

    exp.run()

    exp.save()


for model in models:
    PATH = "../locality-class-drift/locality-concept-drift/datasets/datasets/"
    EXT = "multi_class_*_ds_1_c_10_ca_5_*.csv"
    streams = [
        file
        for path, subdir, files in os.walk(PATH)
        for file in glob(os.path.join(path, EXT))
    ]

    out = Parallel(n_jobs=1)(
        delayed(task)(stream, model, dd)
        for stream, dd in itertools.product(streams, dds)
    )