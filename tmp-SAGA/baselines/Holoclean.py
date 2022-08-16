import sys
sys.path.append('../')
import holoclean
from detect import NullDetector, ViolationDetector
from repair.featurize import *
import sys

path = sys.argv[1]
const = sys.argv[2]
data = sys.argv[3]
out = sys.argv[4]


hc = holoclean.HoloClean(
    db_name='holo',
    domain_thresh_1=0,
    domain_thresh_2=0,
    weak_label_thresh=0.90,
    max_domain=10000,
    cor_strength=0.2,
    nb_cor_strength=0.4,
    epochs=100,
    weight_decay=0.01,
    learning_rate=0.001,
    threads=1,
    batch_size=1,
    verbose=True,
    timeout=3*60000,
    feature_norm=False,
    weight_norm=False,
    print_fw=True
).session

print("starting session")
# 2. Load training data and denial constraints.
hc.load_data(name=data, fpath=path)
hc.load_dcs(const)
hc.ds.set_constraints(hc.get_dcs())

# 3. Detect erroneous cells using these two detectors.
detectors = [NullDetector(), ViolationDetector()] 
hc.detect_errors(detectors)

# 4. Repair errors utilizing the defined features.
hc.setup_domain()
featurizers = [
    OccurAttrFeaturizer(),
    FreqFeaturizer(),
    ConstraintFeaturizer()
]
status, repaired_df = hc.repair_errors(featurizers)
repaired_df.drop("_tid_", axis=1)
repaired_df.to_csv(out, index=False, header=True, sep=",", encoding='utf-8')
