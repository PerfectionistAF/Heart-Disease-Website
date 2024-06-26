from django.apps import AppConfig
import pandas as pd
from joblib import load
import os


# echo libraries
import cv2
import numpy as np
from keras.models import load_model
import joblib
# # ecg necessary libraries
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from keras.applications.vgg16 import VGG16
# from keras.applications.vgg16 import decode_predictions
# from keras.applications.vgg16 import preprocess_input
# from keras.preprocessing import image
# from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D
# from tensorflow.keras.layers import Dense, Flatten
# from tensorflow.keras.models import Model
# import datetime
# import numpy as np
# import os
# import tensorflow as tf
# import matplotlib.pyplot as plt
# from tqdm import tqdm
# #import cv2
# #import PIL.Image
# import matplotlib 
# # import seaborn as sns
# from IPython.display import display
# import matplotlib.pyplot as plt
# # %matplotlib inline
# import shutil
# import posixpath
# import sys 
# import glob
# #import wfdb
# import pandas as pd
# import math
# #from PIL import Image

# from tensorflow.keras.models import load_model




# def set_memory_growth():
#     physical_devices = tf.config.experimental.list_physical_devices('GPU')
#     if physical_devices:
#         try:
#             for device in physical_devices:
#                 tf.config.experimental.set_memory_growth(device, True)
#             logical_devices = tf.config.experimental.list_logical_devices('GPU')
#         except RuntimeError as e:
#             print(e)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

class RiskFactorsPredictionConfig(AppConfig):
    name = 'Risk_Factors_Prediction'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
    CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "gradient_boost_model.sav")
    # classifier = None
    classifier = load(CLASSIFIER_FILE)

    # def ready(self):
    #     set_memory_growth()
    #     if not self.classifier:
    #         self.classifier = load(self.CLASSIFIER_FILE)

# class ECGIIPredictionConfig(AppConfig):
#     name = 'ECG_II'
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
#     CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "resnet50_ii_images.keras")
#     classifier = load_model(CLASSIFIER_FILE)
#     # classifier = None

#     # def ready(self):
#     #     set_memory_growth()
#     #     if not self.classifier:
#     #         self.classifier = load_model(self.CLASSIFIER_FILE)

# class ECGV6PredictionConfig(AppConfig):
#     name = 'ECG_V6'
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
#     CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "resnet50_v6_images.keras")
#     classifier = load_model(CLASSIFIER_FILE)
#     # classifier = None

#     # def ready(self):
#     #     set_memory_growth()
#     #     if not self.classifier:
#     #         self.classifier = load_model(self.CLASSIFIER_FILE)

# class ECGVZPredictionConfig(AppConfig):
#     name = 'ECG_VZ'
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
#     CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "resnet50_vz_images.keras")
#     classifier = load_model(CLASSIFIER_FILE)
#     # classifier = None

#     # def ready(self):
#     #     set_memory_growth()
#     #     if not self.classifier:
#     #         self.classifier = load_model(self.CLASSIFIER_FILE)


# class EchoSegmentationConfig(AppConfig):
#     name = 'Echo_Prediction'
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
#     CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "laddernet_model.keras")
#     # classifier = None
#     classifier = load(CLASSIFIER_FILE)

#     # def ready(self):
#     #     set_memory_growth()
#     #     if not self.classifier:
#     #         self.classifier = load(self.CLASSIFIER_FILE)

# class EchoPredictionConfig(AppConfig):
#     name = 'Echo_Prediction'
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     CLASSIFIER_FOLDER = os.path.join(base_dir, 'users/machine learning models')
#     CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "best_logistic_regression_model.joblib")
#     # CLASSIFIER_FILE = os.path.join(CLASSIFIER_FOLDER, "LinearRegressionClassificationModel_old.pkl")

#     # classifier = None
#     classifier = joblib.load(CLASSIFIER_FILE)
    
#     # def ready(self):
#     #     set_memory_growth()
#     #     if not self.classifier:
#     #         self.classifier = load(self.CLASSIFIER_FILE)