from azureml.core import Run, Workspace, Datastore, Dataset
import pandas as pd
import os
import argparse
import numpy as np
import datetime
import random

# Parse input arguments
parser = argparse.ArgumentParser("Get raw data from a selected datastore and register in AML workspace")
parser.add_argument('--scored_data', dest='scored_data', required=True)
parser.add_argument('--filename', type=str, required=True)

args, _ = parser.parse_known_args()
scored_data = args.scored_data
filename = args.filename

# Get current run
current_run = Run.get_context()

# Get associated AML workspace
ws = current_run.experiment.workspace

# Connect to default blob datastore
ds = ws.get_default_datastore()

################################# MODIFY #################################

# The intent of this block is to load from a target data source. This
# can be from an AML-linked datastore or a separate data source accessed
# using a different SDK. Any initial formatting operations can be be 
# performed here as well.

dataset_one = current_run.input_datasets['Dataset_One']
dataset_one_df = dataset_one.to_pandas_dataframe()
dataset_one_cols = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
dataset_one_val = dataset_one_df.iloc[random.randint(0, len(dataset_one_df))][random.choice(dataset_one_cols)]

dataset_two = current_run.input_datasets['Dataset_Two']
dataset_two_df = dataset_two.to_pandas_dataframe()
dataset_two_cols =  ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
dataset_two_val = dataset_two_df.iloc[random.randint(0, len(dataset_two_df))][random.choice(dataset_two_cols)]

now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
timestamp = now.strftime("%Y%m%d%H%M%S")
timestamp = 'output'

out_df = pd.DataFrame([{'A': dataset_one_val, 'B': dataset_two_val, 'TIME': current_time}])

##########################################################################

# # Make directory on mounted storage for output dataset
os.makedirs(scored_data, exist_ok=True)

# Save modified dataframe
out_df.to_csv(os.path.join(scored_data, filename), index=False)