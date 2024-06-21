from django.apps import AppConfig
import pandas as pd
from joblib import load
import os


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


class RiskFactorsPredictionConfig(AppConfig):
    name = 'Risk_Factors_Prediction'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Base directory:", base_dir)
    CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
    print("Classifier folder:", CLASSIFIER_FOLDER)
    CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "gradient_boost_model.sav")
    print("Classifier file:", CLASSIFIER_FILE)
    classifier = load(CLASSIFIER_FILE)