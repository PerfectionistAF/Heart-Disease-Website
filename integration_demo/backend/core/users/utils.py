#necessary libraries
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
import datetime
import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from tqdm import tqdm
#import cv2
#import PIL.Image
import matplotlib
matplotlib.use('Agg')
# import seaborn as sns
from IPython.display import display
import matplotlib.pyplot as plt
# %matplotlib inline
import shutil
import posixpath
import sys 
import glob
import wfdb
import pandas as pd
import math
#from PIL import Image

from tensorflow.keras.models import load_model


# processing.py
import os
import wfdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


import base64
from PIL import Image



# 0 is healthy
# 1 is sick
MODEL_LABELS = {
    'rf': {
        0: '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)',
        1: '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
    },
    'ecg': {
        0: 'The patient is more likely to be healthy.',
        1: 'The patient is more likely to have Myocardial Infarction (MI).'
    },
    'echo': {
        0: 'Not Myocardial Infarction.',
        1: 'Myocardial Infarction.'
    },
    'integrated': {
        1: 'healthy',
        2: 'low risk/ damage',
        3: 'unqualified/ congenital damage',
        4: 'high risk'
    }
}

#  This function is the truth table
def integ_diagnose(rf_string, ecg_string, echo_string):
    rf_diagnosis = get_integ_diagnosis_key('rf', rf_string)
    ecg_diagnosis = get_integ_diagnosis_key('ecg', ecg_string)
    echo_diagnosis = get_integ_diagnosis_key('echo', echo_string)


    # Case 1: using only one model
    if (rf_diagnosis is None and ecg_diagnosis is None):
        return 1 if echo_diagnosis==0 else 4
    if (rf_diagnosis is None and echo_diagnosis is None):
        return 1 if ecg_diagnosis==0 else 4
    if (ecg_diagnosis is None and echo_diagnosis is None):
        return 1 if rf_diagnosis==0 else 4
    

    # Case 2.a: using two models that produce an intermediate label
    if echo_diagnosis is None:
        return 4 if ecg_diagnosis == 1 else 1
    
    # Case 2.b: using two models that DON’T produce an intermediate label
    if rf_diagnosis is None:
        rf_diagnosis = ecg_diagnosis
    if ecg_diagnosis is None:
        ecg_diagnosis = rf_diagnosis




    intermediate = (ecg_diagnosis == 1)

    if intermediate == 0 and echo_diagnosis == 0:
        integrated = 1
    elif intermediate == 1 and echo_diagnosis == 0:
        integrated = 2
    elif intermediate == 0 and echo_diagnosis == 1:
        integrated = 3
    elif intermediate == 1 and echo_diagnosis == 1:
        integrated = 4

    return integrated

# integ_diagnose (Truth table function) helper
def get_integ_diagnosis_key(model, string):
    for key, value in MODEL_LABELS[model].items():
        if value == string:
            return key
    return None






def custom_load_image(file_path):
    with open(file_path, 'rb') as img_file:
        return img_file.read()


def base64_to_image(base64_string, file_path):
    """
    Decode a base64 string and save it as an image file.

    :param base64_string: The base64 encoded string of the image.
    :param file_path: The path where the image will be saved.
    :return: The path to the saved image.
    """
    image_data = base64.b64decode(base64_string)
    with open(file_path, 'wb') as file:
        file.write(image_data)
    return file_path

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    


def preprocess_dat(dat_file, destination_path, channels):
    record = wfdb.rdrecord(os.path.splitext(dat_file)[0], sampto=1000)
    df = pd.DataFrame(record.p_signal, columns=record.sig_name)

    for channel in channels:
        if channel in df.columns:
            graph = np.array(df[channel])
            plt.plot(graph, label='Channel: ' + channel)

            # Ensure the destination directory exists
            os.makedirs(destination_path, exist_ok=True)
            plt.savefig(os.path.join(destination_path, os.path.basename(dat_file) + f'_{channel}.png'))
            plt.close()





# helper function for Risk_Factors_Model_Predict
def convert_value(value):
    try:
        float_value = float(value)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        # If the value can't be converted to float, return it as is
        return value




# Model predict

def predict_image(image_path, model):   ##overload function
    img = image.load_img(image_path, target_size=(224, 224, 3))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds

def disease_predict(array):
    label = 0
    for i in range(0,2):
        if array[0][0] < array[0][1] :
            label = 1

    return label







def interpret_combined_prediction(preds_ii, preds_v6, preds_vz):
    # Interpret each lead's prediction
    healthy_ii = preds_ii[0][0] > preds_ii[0][1]
    healthy_v6 = preds_v6[0][0] > preds_v6[0][1]
    healthy_vz = preds_vz[0][0] > preds_vz[0][1]
    
    # Determine if the patient is sick based on at least 2 leads indicating sickness
    sick_count = 0
    if not healthy_ii:
        sick_count += 1
    if not healthy_v6:
        sick_count += 1
    if not healthy_vz:
        sick_count += 1
    
    if sick_count >= 2:
        return MODEL_LABELS['ecg'][1] # sick
    else:
        return MODEL_LABELS['ecg'][0] # healthy
                                  
    