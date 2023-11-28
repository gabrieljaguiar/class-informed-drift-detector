from river import tree, drift
from experiment import Experiment
from joblib import Parallel, delayed
import itertools
from glob import glob
import os
from utils.csv import CSVStream
from drift_detectors import NoDrift, TruthDetector
from classifiers import AdaNB, OneVsAllClassifier, AdaGaussianNB

models = [
    ("NB_no_retrain", AdaNB(classifier=AdaGaussianNB(), drift_detector=NoDrift())), 
    ("NB_retrain", AdaNB(classifier=AdaGaussianNB(), drift_detector=NoDrift(), retrain=True)),
    ("NB_gt", AdaNB(classifier=AdaGaussianNB(), drift_detector=TruthDetector(49800, classes_affected=[9,8,7]))), 
    #("OVA", OneVsAllClassifier(classifier=tree.HoeffdingTreeClassifier()))
]

dds = [
    #("No_drift", NoDrift()),
    ("ground_truth", TruthDetector(49800, classes_affected=[9,8,7]))
]


def task(stream_path, model, dd):
    stream = CSVStream("{}".format(stream_path))
    stream_name = os.path.splitext(os.path.basename(stream_path))[0]
    stream_output = "./output/"
    print(stream_output)
    model_name, model = model
    model = model.clone()
    dd_name, dd = dd
    dd = dd.clone()
    #model.driftDetector = dd.clone()
    exp_name = "{}_{}_{}".format(model_name, dd_name, stream_name)
    print("Running {}...".format(exp_name))
    exp = Experiment(exp_name, stream_output, model, dd, stream, stream_size=100000)

    exp.run()

    exp.save()


for model in models:
    PATH = "../locality-class-drift/locality-concept-drift/datasets/datasets/"
    EXT = "multi_class_*_ds_1_c_10_ca_2_*.csv"
    streams = [
        file
        for path, subdir, files in os.walk(PATH)
        for file in glob(os.path.join(path, EXT))
    ]

    out = Parallel(n_jobs=1)(
        delayed(task)(stream, model, dd)
        for stream, dd in itertools.product(streams, dds)
    )