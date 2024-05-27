import pytest
from performance_model import evaluate_model
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from config.loader import config

model_file_name = f"{config.cloud_config.bucket_model_name}_{config.modeling_config.version_model}.pkl"
PATH_MODEL = os.path.join('fitted_models/', model_file_name)


@pytest.fixture
def model_name():
    return PATH_MODEL

def test_evaluate_model(model_name):
    precision, recall, f1 = evaluate_model(model_name)

    assert precision >= config.performance_config.threshold_precision, f"La precision ({precision}) es menor que el umbral ({config.performance_config.threshold_precision})"
    assert recall >= config.performance_config.threshold_recall, f"El recall ({recall}) es menor que el umbral ({config.performance_config.threshold_recall})"
    assert f1 >= config.performance_config.threshold_f1, f"El F1 score ({f1}) es menor que el umbral ({config.performance_config.threshold_f1})"


test_evaluate_model(PATH_MODEL)
