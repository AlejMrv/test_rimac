import joblib
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from config.loader import config
from gcp_utils import cloud_functions


def evaluate_model(model_file_name):
    
    model_fitted = joblib.load(model_file_name)

    dataset = cloud_functions.get_dataset_from_bigquery(project_id=config.cloud_config.project_id
                                                        , dataset_id=config.cloud_config.bigquery_dataset
                                                        , table_name=config.cloud_config.bigquery_dataset_test_table)


    y_pred = model_fitted.predict(X=dataset[config.modeling_config.features])
    y_true = dataset[config.modeling_config.target].astype('int64')

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return precision, recall, f1