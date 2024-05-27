import pandas as pd
import sys
import os
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from pipeline_functions import *

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from config.loader import config
from gcp_utils import cloud_functions



def fit_model():

    #dataset = pd.read_csv(filepath_or_buffer=config.app_config.data_raw)
    # Cargar dataset de Bigquery
    dataset = cloud_functions.get_dataset_from_bigquery(project_id=config.cloud_config.project_id
                                                        , dataset_id=config.cloud_config.bigquery_dataset
                                                        , table_name=config.cloud_config.bigquery_dataset_table)
    # Dividir en train y test
    X_train, X_test, y_train, y_test = train_test_split(
                                        dataset[config.modeling_config.features], 
                                        dataset[config.modeling_config.target],
                                        test_size = config.modeling_config.test_size,
                                        random_state = config.modeling_config.random_state
                                        )
    y_train = y_train.astype('int64')

    # Regitrando datasets en gcp
    process_dataset_in_gcp(X_train, X_test, y_train, y_test)

    # Definir procesamiento segun tipo de datos
    numerical_features, categorical_features = config.modeling_config.numerical_features, config.modeling_config.categorical_features
    col_transformer = make_column_transformer((OneHotEncoder(), categorical_features)
                                            ,(StandardScaler(), numerical_features)
                                            ) 
    # Crear pipeline y obtener modelo
    model_pipeline = make_pipeline(col_transformer, LGBMClassifier())
    model_pipeline.fit(X_train, y_train)

    # Guardar modelo
    model_file_name = f"{config.app_config.model_fitted_name}_{config.modeling_config.version_model}.pkl"
    joblib.dump(model_pipeline, model_file_name)

    # Registrar en bucket
    cloud_functions.upload_cs_file(bucket_name=config.cloud_config.bucket_name
            , source_file_name=model_file_name
            , destination_file_name=f"{config.cloud_config.bucket_model_name}_{config.modeling_config.version_model}.pkl"
            , overwrite=True
        )


if __name__ == "__main__":
    fit_model()