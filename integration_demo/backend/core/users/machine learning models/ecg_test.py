# #necessary libraries
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
# import wfdb
# import pandas as pd
# import math
# #from PIL import Image

# from tensorflow.keras.models import load_model


# current_dir = os.path.dirname(os.path.abspath(__file__)) # if using .py
# # current_dir = os.getcwd() # if using ipynb

# resnet50_ii_filename = os.path.join(current_dir, "resnet50_ii_images.keras")
# resnet50_v6_filename = os.path.join(current_dir, "resnet50_v6_images.keras")
# resnet50_vz_filename = os.path.join(current_dir, "resnet50_vz_images.keras")

# file_ii = os.path.join(current_dir, "ecg_image/ii/28.csv.png")
# file_v6 = os.path.join(current_dir, "ecg_image/v6/28.csv.png")
# file_vz = os.path.join(current_dir, "ecg_image/vz/28.csv.png")

# print(f"resnet50_ii_filename: {resnet50_ii_filename}")
# print(f"resnet50_v6_filename: {resnet50_v6_filename}")
# print(f"resnet50_vz_filename: {resnet50_vz_filename}")

# print(f"file_ii: {file_ii}")
# print(f"file_v6: {file_v6}")
# print(f"file_vz: {file_vz}")


# # Preprocessing: from signal records to csv

# #PTB DATASET
# #Convert all to csv then to txt
# def preprocess_dat_to_csv():

#     # Define the relative path to the directory containing ECG .dat files
#     relative_ptb_path = os.path.join(current_dir, 'ecg_dat', '*.dat')

#     # Find all .dat files matching the pattern in the relative directory
#     ptb_files = glob.glob(relative_ptb_path)

#     # Debugging: print the path being searched and the files found
#     print(f"Searching for files in: {os.path.dirname(relative_ptb_path)}")
#     print(f"Number of files found: {len(ptb_files)}")

#     # Print the contents of the directory
#     directory_path = os.path.dirname(relative_ptb_path)
#     try:
#         print(f"Contents of directory {directory_path}:")
#         print(os.listdir(directory_path))
#     except FileNotFoundError:
#         print(f"Error: The directory {directory_path} does not exist. Please check the path.")

#     # Proceed if files are found
#     if ptb_files:
#         # List to store WFDB records
#         ptb_record_list = []

#         # Read each file and store the record
#         for file in ptb_files:
#             name = os.path.splitext(file)[0]
#             ptb_record_list.append(wfdb.rdrecord(name, sampto=1000))

#         # List to store DataFrames
#         ptb_df_list = []

#         # Convert records to DataFrames and save as CSV files
#         for i, record in enumerate(ptb_record_list):
#             df = pd.DataFrame(record.p_signal, columns=record.sig_name)
#             ptb_df_list.append(df)

#             # Define the relative paths for the directories
#             csv_directory = os.path.join(current_dir, 'ptb_ecg_db_csv')
#             txt_directory = os.path.join(current_dir, 'ptb_ecg_db_txt')

#             # Create directories if they don't exist
#             os.makedirs(csv_directory, exist_ok=True)
#             os.makedirs(txt_directory, exist_ok=True)

#             # Save CSV file
#             csv_name = os.path.join(csv_directory, f'{i}.csv')
#             df.to_csv(csv_name, index=False)

#         # Convert CSV files to TXT files
#         for i in range(len(ptb_record_list)):
#             csv_name = os.path.join(csv_directory, f'{i}.csv')
#             txt_name = os.path.join(txt_directory, f'{i}.txt')
#             with open(csv_name, 'r') as f_in, open(txt_name, 'w') as f_out:
#                 content = f_in.read()
#                 f_out.write(content)

#         print("Processing complete.")
#     else:
#         print("No files found. Please check the directory and file pattern.")


# # Preprocessing: csv to images

# ##Resize images to default pretrained tensor size: 224, 224, 3
# def new_images(path):
#     for image in os.listdir(path):
#         print(image)
#         name = os.path.basename(image)
#         image = Image.open(path +'/' + image)
#         resized_image = image.resize((224, 224))
#         resized_image.save(path +'/' + name)

# ##extract images of separate channels from csv without transformation--data is already clean
# def extract_images(source_path, destination_path, channel):
#     for file in os.listdir(source_path):
#         #open csv from the source_path
#         df = pd.read_csv(source_path+'/'+file)
#         #that channel values are converted to arrays to ease graphing
#         graph = np.array(df[channel])
#         #plot the channel points
#         image = plt.plot(graph, label='Channel:'+ channel)
#         #save the image in the destination
#         plt.savefig(destination_path+'/'+file+'.png')
#         #graph is reset and plot is closed to avoid overlap
#         plt.close()
#         graph = 0
#         image = 0
        
#     return 

# ##same as extract_images except with 2 channels at the same time to test reciprocity
# def multi_extract_images(source_path, destination_path, channel1, channel2):
#     for file in os.listdir(source_path):
#         #open csv from the source_path
#         df = pd.read_csv(source_path+'/'+file)
#         #that channel values are converted to arrays to ease graphing
#         graph1 = np.array(df[channel1])
#         graph2 = np.array(df[channel2])
#         #plot the channel points
#         image = plt.plot(graph1, label='Channel:'+ channel1)
#         image = plt.plot(graph2, label='Channel:'+ channel2)
#         #save the image in the destination
#         plt.savefig(destination_path+'/'+file+'.png')
#         #graph is reset and plot is closed to avoid overlap
#         plt.close()
#         graph = 0
#         image = 0
        
#     return


# Model predict

# def predict_image(image_path, model):   ##overload function
#     img = image.load_img(image_path, target_size=(224, 224, 3))
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     preds = model.predict(x)
#     return preds

# def disease_predict(array):
#     label = 0
#     for i in range(0,2):
#         if array[0][0] < array[0][1] :
#             label = 1

#     return label

# def generate_label(predict_array):
#     label = 0
#     count = 0
#     for i in range(predict_array.shape[1]):
#         if predict_array[0][i] == 1 :
#             count = count + 1
#     if count >= (2 * 3) * predict_array.shape[1]:  
#         label = 1
#     return label





# # main

# # Preprocessing
# # dat to csv
# preprocess_dat_to_csv()

# # csv to img
# # for ecg_csv files
# extract_images(os.path.join(current_dir, 'ecg_csv'),
#                os.path.join(current_dir, 'ecg_image/ii'),
#                'ii')
# extract_images(os.path.join(current_dir, 'ecg_csv'),
#                os.path.join(current_dir, 'ecg_image/v6'),
#                'v6')
# extract_images(os.path.join(current_dir, 'ecg_csv'),
#                os.path.join(current_dir, 'ecg_image/vz'),
#                'vz')
# # for ecg_dat -> ptb_ecg_db_csv files
# extract_images(os.path.join(current_dir, 'ptb_ecg_db_csv'),
#                os.path.join(current_dir, 'ecg_image/ii'),
#                'ii')
# extract_images(os.path.join(current_dir, 'ptb_ecg_db_csv'),
#                os.path.join(current_dir, 'ecg_image/v6'),
#                'v6')
# extract_images(os.path.join(current_dir, 'ptb_ecg_db_csv'),
#                os.path.join(current_dir, 'ecg_image/vz'),
#                'vz')


# # Load the three models
# model_ii = load_model(resnet50_ii_filename)
# model_v6 = load_model(resnet50_v6_filename)
# model_vz = load_model(resnet50_vz_filename)

# # Predict 1/3
# preds_ii = predict_image(file_ii, model_ii)
# print("ii: ", preds_ii)

# # Predict 2/3
# preds_v6 = predict_image(file_v6, model_v6)
# print("v6: ", preds_v6)

# # Predict 3/3
# preds_vz = predict_image(file_vz, model_vz)
# print("vz: ", preds_vz)



# def interpret_combined_prediction(preds_ii, preds_v6, preds_vz):
#     # Interpret each lead's prediction
#     healthy_ii = preds_ii[0][0] > preds_ii[0][1]
#     healthy_v6 = preds_v6[0][0] > preds_v6[0][1]
#     healthy_vz = preds_vz[0][0] > preds_vz[0][1]
    
#     # Determine if the patient is sick based on at least 2 leads indicating sickness
#     sick_count = 0
#     if not healthy_ii:
#         sick_count += 1
#     if not healthy_v6:
#         sick_count += 1
#     if not healthy_vz:
#         sick_count += 1
    
#     if sick_count >= 2:
#         return "The patient is more likely to have Myocardial Infarction (MI)."
#     else:
#         return "The patient is more likely to be healthy."                                   
    
# # Combine predictions and interpret result
# combined_status = interpret_combined_prediction(preds_ii, preds_v6, preds_vz)
# print(combined_status)




"""Process a single dat file into 3 images"""
import os
import wfdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))  # if using .py
# current_dir = os.getcwd()  # if using ipynb


def preprocess_single_file(dat_file, destination_path, channels):
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

# Example usage: preprocess a single .dat file
single_dat_file = os.path.join(current_dir, 'ecg_dat', 's0028lre.dat')

# Preprocess and extract images for the single .dat file
preprocess_single_file(single_dat_file, os.path.join(current_dir, 'ecg_image/ii'), ['ii'])
preprocess_single_file(single_dat_file, os.path.join(current_dir, 'ecg_image/v6'), ['v6'])
preprocess_single_file(single_dat_file, os.path.join(current_dir, 'ecg_image/vz'), ['vz'])

