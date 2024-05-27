
# %%
import yaml
from pydantic import BaseModel
from typing import List

import sys
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_FILE_PATH = os.path.join(project_dir, 'config.yml')
# PATH_DATA_RAW = os.path.join( '..', 'data', 'raw/')
# PATH_DATA_PROCESSED = os.path.join( '..', 'data', 'processed/')
# PATH_MODELS_FITTED = os.path.join('..', 'fitted_models/')

PATH_DATA_RAW = os.path.join( 'data', 'raw/')
PATH_DATA_PROCESSED = os.path.join( 'data', 'processed/')
PATH_MODELS_FITTED = os.path.join('fitted_models/')


class AppConfig(BaseModel):

    data_raw: str
    data_train: str
    data_test: str
    model_fitted_name: str


class ModelConfig(BaseModel):

    target: str
    test_size: float
    random_state: int
    features: List[str]
    numerical_features: List[str]
    categorical_features: List[str]
    version_model: float


class PerformanceConfig(BaseModel):

    threshold_precision: float
    threshold_recall: float
    threshold_f1: float


class CloudConfig(BaseModel):

    project_id: str
    bucket_name: str
    bucket_file_name: str
    bigquery_dataset: str
    bigquery_dataset_table: str
    bucket_model_name: str
    bucket_train_file_name: str
    bucket_test_file_name: str
    bigquery_dataset_train_table: str
    bigquery_dataset_test_table: str

class Config(BaseModel):
    app_config: AppConfig
    modeling_config: ModelConfig
    performance_config: PerformanceConfig
    cloud_config: CloudConfig


def load_config():
    with open(CONFIG_FILE_PATH, 'r') as f:
        config_dict = yaml.safe_load(f)

    app_config_dict  = config_dict.get('app_config', {})
    model_config_dict  = config_dict.get('model_config', {})
    performance_config_dict  = config_dict.get('performance_config', {})
    cloud_config_dict  = config_dict.get('cloud_config', {})

    app_config_instance = AppConfig(**app_config_dict)
    model_config_instance = ModelConfig(**model_config_dict)
    performance_config_instance = PerformanceConfig(**performance_config_dict)
    cloud_config_instance = CloudConfig(**cloud_config_dict)

    # Modificar los valores internos de AppConfig
    app_config_instance.data_raw = PATH_DATA_RAW + app_config_instance.data_raw
    app_config_instance.data_train = PATH_DATA_PROCESSED + app_config_instance.data_train
    app_config_instance.data_test = PATH_DATA_PROCESSED + app_config_instance.data_test
    app_config_instance.model_fitted_name = PATH_MODELS_FITTED + app_config_instance.model_fitted_name

    config_instance = Config(app_config=app_config_instance
                            , modeling_config=model_config_instance
                            , performance_config=performance_config_instance
                            , cloud_config=cloud_config_instance
                            )
    
    return config_instance

config = load_config()
