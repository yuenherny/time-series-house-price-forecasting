import os
from pathlib import Path

import joblib
import pandas as pd
import skops.io as sio

ROOT_DIR = Path(os.getcwd())
APP_DIR = ROOT_DIR / 'app'
DATA_DIR = APP_DIR / 'data'
MODEL_DIR = APP_DIR / 'model'

df_transactions = pd.read_parquet(DATA_DIR / 'transactions_KL_ckpt7_integrated.parquet')
df_monthly_price_psf = pd.read_parquet(DATA_DIR / 'monthly_price_psf.parquet')


def get_transactions():
    return df_transactions


def get_mean_median_monthly_price_psf():
    return df_monthly_price_psf['mean_price_psf'], df_monthly_price_psf['median_price_psf']


def get_encoder(encoder_path):
    if os.path.exists(encoder_path):
        return joblib.load(encoder_path)
    else:
        raise Exception(f'Encoder not found at {encoder_path}')


def get_model(model_path):
    if os.path.exists(model_path):
        return sio.load(model_path, trusted=sio.get_untrusted_types(file=model_path))
    else:
        raise Exception(f'ML model not found at {model_path}')


def get_scaler(scaler_path):
    if os.path.exists(scaler_path):
        return sio.load(scaler_path, trusted=sio.get_untrusted_types(file=scaler_path))
    else:
        raise Exception(f'Scaler not found at {scaler_path}')


def get_township():
    return df_transactions['township'].drop_duplicates().sort_values(ascending=True)


def get_building_type(township):
    return df_transactions.query(f"township == '{township}'")['building_type'].drop_duplicates()


def get_tenure(township):
    return df_transactions.query(f"township == '{township}'")['tenure'].drop_duplicates()


def get_max_floors(township, building_type):
    return int(df_transactions.query(
        f"township == '{township}' and building_type == '{building_type}'"
    )['floors'].max(numeric_only=True))


def get_max_rooms(township, building_type):
    return int(df_transactions.query(
        f"township == '{township}' and building_type == '{building_type}'"
    )['rooms'].max(numeric_only=True))


def get_months_difference(start_date, end_date):
    return abs(end_date.year - start_date.year) * 12 + abs(end_date.month - start_date.month)