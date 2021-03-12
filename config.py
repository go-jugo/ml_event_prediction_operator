from itertools import product
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import os


default_scaler = os.getenv("ML_DEFAULT_SCALER", "StandardScaler")
default_ml_algorithm = os.getenv("ML_DEFAULT_ALGORITHM", "RandomForestClassifier")
logging_level = os.getenv("ML_LOGGING_LEVEL", "info")
logging_color = int(os.getenv("ML_LOGGING_COLOR", 0))
v_dask = os.getenv("ML_V_DASK", True)

debug_mode = False
write_monitoring = False
store_results = False


ml_algorithm_map = {
    "RandomForestClassifier": RandomForestClassifier
}

scaler_map = {
    "StandardScaler": StandardScaler
}

def create_configs():
    base_config = dict(
        sampling_frequency=['30S'],
        imputations_technique_str=['pad'],
        imputation_technique_num=['pad'],
        ts_fresh_window_length=[3600],
        ts_fresh_window_end=[3600],
        ts_fresh_minimal_features=[True],
        scaler=[StandardScaler()],
        target_col=['module_4_errorcode'],
        target_errorCode=[2],
        balance_ratio = [0.5],
        random_state = [[0]],
        cv=[5],
        oversampling_method = [False],
        ml_algorithm=[RandomForestClassifier()]
        )
    configs_pipeline = [dict(zip(base_config, v)) for v in product(*base_config.values())]
    return configs_pipeline

configs_pipeline = create_configs()

