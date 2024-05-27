# %%
import pandas as pd
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from gcp_utils import cloud_functions
from config.loader import config


# %%

def processing_dataset():

    #dataset = pd.read_csv(filepath_or_buffer=config.app_config.data_raw)
    

    cloud_functions.create_bucket(bucket_name=config.cloud_config.bucket_name)

    cloud_functions.upload_cs_file(bucket_name=config.cloud_config.bucket_name
                   , source_file_name=config.app_config.data_raw
                   , destination_file_name=config.cloud_config.bucket_file_name
                   , overwrite=True
                )

    cloud_functions.create_bigquery_dataset_table(dataset_id=config.cloud_config.bigquery_dataset
                                  , table_name=config.cloud_config.bigquery_dataset_table
                                  , bucket_name=config.cloud_config.bucket_name
                                  , file_name=config.cloud_config.bucket_file_name
                                  )


if __name__ == "__main__":
    processing_dataset()