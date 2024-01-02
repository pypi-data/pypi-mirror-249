# Inference on an Endpoint
#
# - Pull data from a Test DataSet
# - Run inference on an Endpoint
# - Capture performance metrics in S3 SageWorks Model Bucket

from sageworks.core.artifacts.feature_set_core import FeatureSetCore
from sageworks.core.artifacts.model_core import ModelCore
from sageworks.core.artifacts.endpoint_core import EndpointCore
import awswrangler as wr

# Test DatsSet
# There's a couple of options here:
# 1. Pull the data from S3 directly
# 2. Backtrack to the FeatureSet and pull data from it


# S3_DATA_PATH = "s3://sageworks-data-science-dev/data-sources/abalone_holdout_2023_10_19.csv"
S3_DATA_PATH = None

# Just for Storage
DATA_NAME = "abalone_features (20)"
DATA_HASH = "12345"
DESCRIPTION = "Test Abalone Features"
TARGET_COLUMN = "class_number_of_rings"

# These should be filled in by the user
# DATA_NAME = "blah (20)"
# DATA_HASH = "12345"
# DESCRIPTION = "Test Solubility Features"
# TARGET_COLUMN = "log_s"


# Spin up our Endpoint
my_endpoint = EndpointCore("abalone-regression-end")
# my_endpoint = EndpointCore("solubility-test-regression-end")

if S3_DATA_PATH is not None:
    # Read the data from S3
    df = wr.s3.read_csv(S3_DATA_PATH)
else:
    # Grab the FeatureSet by backtracking from the Endpoint
    model = my_endpoint.get_input()
    feature_set = ModelCore(model).get_input()
    features = FeatureSetCore(feature_set)
    table = features.get_training_view_table()
    df = features.query(f"SELECT * FROM {table} where training = 0")


# Capture the performance metrics for this Endpoint
my_endpoint.capture_performance_metrics(
    df, TARGET_COLUMN, data_name=DATA_NAME, data_hash=DATA_HASH, description=DESCRIPTION
)
