import pandas as pd
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from config.loader import config
from gcp_utils import cloud_functions



def process_dataset_in_gcp(X_train, X_test, y_train, y_test):

    # Guardando particiones
    train_df = pd.DataFrame(X_train, columns=config.modeling_config.features)
    train_df[config.modeling_config.target] = y_train

    test_df = pd.DataFrame(X_test, columns=config.modeling_config.features)
    test_df[config.modeling_config.target] = y_test

    train_df.to_csv(config.app_config.data_train, index=False)
    test_df.to_csv(config.app_config.data_test , index=False)

    # Registrandolas en Bucket
    cloud_functions.upload_cs_file(bucket_name=config.cloud_config.bucket_name
                   , source_file_name=config.app_config.data_train
                   , destination_file_name=config.cloud_config.bucket_train_file_name
                   , overwrite=True
                )

    cloud_functions.upload_cs_file(bucket_name=config.cloud_config.bucket_name
                   , source_file_name=config.app_config.data_test
                   , destination_file_name=config.cloud_config.bucket_test_file_name
                   , overwrite=True
                )

    cloud_functions.create_bigquery_dataset_table(dataset_id=config.cloud_config.bigquery_dataset
                                  , table_name=config.cloud_config.bigquery_dataset_train_table
                                  , bucket_name=config.cloud_config.bucket_name
                                  , file_name=config.cloud_config.bucket_train_file_name
                                  )
    cloud_functions.create_bigquery_dataset_table(dataset_id=config.cloud_config.bigquery_dataset
                                  , table_name=config.cloud_config.bigquery_dataset_test_table
                                  , bucket_name=config.cloud_config.bucket_name
                                  , file_name=config.cloud_config.bucket_test_file_name
                                  )