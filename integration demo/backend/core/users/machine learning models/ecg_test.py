from tkinter import Image
# from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import posixpath
import glob
import wfdb
import pandas as pd
#necessary libraries
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras import layers
# from keras.applications.vgg16 import VGG16
# from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
# from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D
# from tensorflow.keras.layers import Dense, Flatten
# from tensorflow.keras.models import Model
import datetime
import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
# from tqdm import tqdm
#import cv2
#import PIL.Image
# import matplotlib 
# import seaborn as sns
# from IPython.display import display
import matplotlib.pyplot as plt
import shutil
import posixpath
import sys 
import glob
#import wfdb
import pandas as pd
# import math
#from PIL import Image
import tensorflow as tf
from tensorflow import keras
# from keras.applications.resnet50 import ResNet50
# from keras.applications.resnet50 import preprocess_input, decode_predictions
# from tensorflow.keras import layers, saving
# from tensorflow.keras.layers import Dense, Flatten
# from tensorflow.keras.optimizers import Adam, SGD
import numpy as np
# from keras.models import Sequential

from tensorflow.keras.models import load_model



resnet50_ii_filename = "backend/core/users/machine learning models/resnet50_ii_images.keras"
resnet50_v6_filename = "backend/core/users/machine learning models/resnet50_v6_images.keras"
resnet50_vz_filename = "backend/core/users/machine learning models/resnet50_vz_images.keras"


##Resize images to default pretrained tensor size: 224, 224, 3
def new_images(path):
    for image in os.listdir(path):
        print(image)
        name = os.path.basename(image)
        image = Image.open(path +'/' + image)
        resized_image = image.resize((224, 224))
        resized_image.save(path +'/' + name)

##extract images of separate channels from csv without transformation--data is already clean
def extract_images(source_path, destination_path, channel):
    for file in os.listdir(source_path):
        #open csv from the source_path
        df = pd.read_csv(source_path+'/'+file)
        #that channel values are converted to arrays to ease graphing
        graph = np.array(df[channel])
        #plot the channel points
        image = plt.plot(graph, label='Channel:'+ channel)
        #save the image in the destination
        plt.savefig(destination_path+'/'+file+'.png')
        #graph is reset and plot is closed to avoid overlap
        plt.close()
        graph = 0
        image = 0
        
    return 

##same as extract_images except with 2 channels at the same time to test reciprocity
def multi_extract_images(source_path, destination_path, channel1, channel2):
    for file in os.listdir(source_path):
        #open csv from the source_path
        df = pd.read_csv(source_path+'/'+file)
        #that channel values are converted to arrays to ease graphing
        graph1 = np.array(df[channel1])
        graph2 = np.array(df[channel2])
        #plot the channel points
        image = plt.plot(graph1, label='Channel:'+ channel1)
        image = plt.plot(graph2, label='Channel:'+ channel2)
        #save the image in the destination
        plt.savefig(destination_path+'/'+file+'.png')
        #graph is reset and plot is closed to avoid overlap
        plt.close()
        graph = 0
        image = 0
        
    return



# # TODO from signal records to csv
# #PTB DATASET
# #Convert all to csv then to txt


# ptb_path = r'ptb_ecg_db//' ##all files
# ptb_files = glob.glob(ptb_path)

# #print(files)
# len(ptb_files)

# ptb_files[289]
# result = os.path.splitext(ptb_files[289])[0]
# print(result)

# ptb_record_list = [] ##use record list only
# for i in range(len(ptb_files)):
#     name = os.path.splitext(ptb_files[i])[0]
#     ptb_record_list.append(wfdb.rdrecord(name, sampto=1000))
# #annotation_ptb222 = wfdb.rdann('ptb_ecg_db/patient169/s0329lre', 'dat', sampto = 10000)###refer to CNN_input_gen

# ptb_df_list = []
# for i in range(len(ptb_record_list)):
#     ptb_df_list.append(pd.DataFrame(ptb_record_list[i].p_signal, columns=ptb_record_list[i].sig_name))
#     name = 'ptb_ecg_db_csv/' + str(i) + '.csv'
#     ptb_df_list[i].to_csv(name, index=False)

# for i in range(len(ptb_record_list)):
#     name = 'ptb_ecg_db_csv/' + str(i) + '.csv'
#     name2 = 'ptb_ecg_db_txt/' + str(i) + '.txt'
#     with open(name, 'r') as f_in, open(name2, 'w') as f_out:
#         content = f_in.read()
#         f_out.write(content)



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

# def generate_label(predict_array):
#     label = 0
#     count = 0
#     for i in range(predict_array.shape[1]):
#         if predict_array[0][i] == 1 :
#             count = count + 1
#     if count >= (2 * 3) * predict_array.shape[1]:  
#         label = 1
#     return label





# main

# # Preprocessing
# # csv to img
# extract_images('backend/core/users/machine learning models/ecg_csv',
#                'backend/core/users/machine learning models/ecg_image/ii',
#                'ii')
# extract_images('backend/core/users/machine learning models/ecg_csv/',
#                'backend/core/users/machine learning models/ecg_image/v6',
#                'v6')
# extract_images('backend/core/users/machine learning models/ecg_csv',
#                'backend/core/users/machine learning models/ecg_image/vz',
#                'vz')
# predict using img
model_ii = load_model(resnet50_ii_filename)
model_v6 = load_model(resnet50_v6_filename)
model_vz = load_model(resnet50_vz_filename)

print("ii:")
# for file in os.listdir("backend/core/users/machine learning models/ecg_image/ii"):
file_ii = "backend/core/users/machine learning models/ecg_image/ii/28.csv.png"
predict_image(file_ii, model_ii)

print("v6")
# for file in os.listdir("backend/core/users/machine learning models/ecg_image/v6"):
file_v6 = "backend/core/users/machine learning models/ecg_image/v6/28.csv.png"
predict_image(file_v6, model_v6)

print("vz")
# for file in os.listdir("backend/core/users/machine learning models/ecg_image/vz"):
file_vz = "backend/core/users/machine learning models/ecg_image/vz/28.csv.png"
predict_image(file_vz, model_vz)



