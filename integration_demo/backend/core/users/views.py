from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import User, Patient, DoctorPatientFile
from .serializers import EchoFileUploadSerializer, UserSerializer, LoginSerializer, PatientSerializer, DoctorPatientFileSerializer, ECGFileUploadSerializer, DoctorPatientFileSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PatientFilter, DoctorPatientFileFilter
from .apps import RiskFactorsPredictionConfig#, ECGIIPredictionConfig, ECGV6PredictionConfig, ECGVZPredictionConfig
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status
# views.py
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ECGFileUploadSerializer
from .utils import convert_value, integ_diagnose, preprocess_dat, predict_image, interpret_combined_prediction, image_to_base64, base64_to_image, custom_load_image, MODEL_LABELS

import tempfile

from django.core import files


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



#echo libraries
import cv2





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data  # Include user data in the response
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)








class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PatientFilter
    ordering_fields = ['doctor', 'name', 'created_at']
    ordering = ['name']

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorPatientFileListCreateView(generics.ListCreateAPIView):
    queryset = DoctorPatientFile.objects.all()
    serializer_class = DoctorPatientFileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DoctorPatientFileFilter
    ordering_fields = ['doctor', 'patient', 'final_diagnosis', 'prognosis', 'created_at']
    ordering = ['created_at']
    parser_classes = (MultiPartParser, FormParser)



class DoctorPatientFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorPatientFile.objects.all()
    serializer_class = DoctorPatientFileSerializer













# Class based view to predict based on Risk Factors model
class Risk_Factors_Model_Predict(APIView):
    #permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data = request.data
        

        df = pd.DataFrame([data])
        converted_df = df.map(convert_value)

        # Preprocessing
        combined_df = converted_df.copy()
        combined_df['total_risk'] = combined_df['trestbps'] + combined_df['chol']
        threshold_heart_rate = 150
        combined_df['exercise_angina'] = (combined_df['exang'] == 1) & (combined_df['thalach'] > threshold_heart_rate)
        combined_df['cholesterol_hdl_ratio'] = combined_df['chol'] / combined_df['thalach']
        data = combined_df

        # Predict
        classifier = RiskFactorsPredictionConfig.classifier
        y_pred = classifier.predict(data)
        y_pred = pd.Series(y_pred)
        target_map = {0: MODEL_LABELS['rf'][0], # healthy
                      1: MODEL_LABELS['rf'][1] } # sick

        y_pred = y_pred.map(target_map).to_numpy()
        response_dict = {"Risk Factors Prediction": y_pred[0]}



        return Response(response_dict, status=200)












class ECGFileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ECGFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            dat_file = serializer.validated_data['dat_file']
            hea_file = serializer.validated_data['hea_file']
            xyz_file = serializer.validated_data.get('xyz_file', None)  # Handle optional xyz_file

            # Directory where files will be saved
            save_path = os.path.join(settings.MEDIA_ROOT, 'ecg/input')
            os.makedirs(save_path, exist_ok=True)

            # Save the signal files without using a model
            file_data = {
                'dat_file': dat_file,
                'hea_file': hea_file,
                'xyz_file': xyz_file,
            }
            for file_key, uploaded_file in file_data.items():
                if uploaded_file is not None:  # Check if the file is not None
                    file_path = os.path.join(save_path, uploaded_file.name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
            
            # Process the images
            file_path = os.path.join(save_path, dat_file.name)
            destination_path = os.path.join(settings.MEDIA_ROOT, 'ecg/output')
            # Save the images (the first time, for prediciton)
            preprocess_dat(file_path, destination_path, ['ii'])
            preprocess_dat(file_path, destination_path, ['v6'])
            preprocess_dat(file_path, destination_path, ['vz'])

           
            # Combine predictions and interpret result
            # combined_status = MODEL_LABELS['ecg'][0] # healthy
            combined_status = MODEL_LABELS['ecg'][0] # sick

            # Send back diagnosis and images to be saved in doctor-patient-file in db...
            image_ii_path = os.path.join(destination_path, dat_file.name + "_ii.png")
            image_v6_path = os.path.join(destination_path, dat_file.name + "_v6.png")
            image_vz_path = os.path.join(destination_path, dat_file.name + "_vz.png")
            # image_ii_base64 = image_to_base64(image_ii_path)
            # image_v6_base64 = image_to_base64(image_v6_path)
            # image_vz_base64 = image_to_base64(image_vz_path)
            response_dict = {
                "ECG Prediction": combined_status,
                "image_ii": image_ii_path,
                "image_v6": image_v6_path,
                "image_vz": image_vz_path
            }

            # Finally, just delete the unneeded files
            os.remove(os.path.join(save_path, dat_file.name))
            os.remove(os.path.join(save_path, hea_file.name))
            os.remove(os.path.join(save_path, xyz_file.name))

            return Response(response_dict, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            # Load models
            # model_ii = ECGIIPredictionConfig.classifier
            # model_v6 = ECGV6PredictionConfig.classifier
            # model_vz = ECGVZPredictionConfig.classifier
            # # Predict
            # preds_ii = predict_image(os.path.join(destination_path, dat_file.name + "_ii.png"), model_ii)
            # preds_v6 = predict_image(os.path.join(destination_path, dat_file.name + "_v6.png"), model_v6)
            # preds_vz = predict_image(os.path.join(destination_path, dat_file.name + "_vz.png"), model_vz)
            # # Combine predictions and interpret result
            # combined_status = interpret_combined_prediction(preds_ii, preds_v6, preds_vz)
            # TODO until you setup the model loading, here's a hardcoded prediction...










class EchoFileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = EchoFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.validated_data['video']

            # Directory where files will be saved
            save_path = os.path.join(settings.MEDIA_ROOT, 'videos')
            os.makedirs(save_path, exist_ok=True)

            # Save the video file without using a model
            if video is not None:  # Check if the file is not None
                file_path = os.path.join(save_path, video.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in video.chunks():
                        destination.write(chunk)
            
            # Process the video.... segment...

           
            # Combine predictions and interpret result
            # result = MODEL_LABELS['echo'][0] # healthy
            result = MODEL_LABELS['echo'][1] # sick
            
            response_dict = {
                "Echo Prediction": result,
                "video": os.path.join(save_path, video.name)
               
            }

            return Response(response_dict, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            # Load models
            # TODO until you setup the model loading, here's a hardcoded prediction...











class DoctorPatientFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        # Find final prediction from rf_diagnosis, ecg_diagnosis, video_diagnosis using conditional table method
        rf_diagnosis = request.data.get('rf_diagnosis') if request.data.get('rf_diagnosis') else ''
        ecg_diagnosis = request.data.get('ecg_diagnosis') if request.data.get('ecg_diagnosis') else ''
        echo_diagnosis = request.data.get('echo_diagnosis') if request.data.get('echo_diagnosis') else ''
        print("rf_diagnosis: ", rf_diagnosis, "ecg_diagnosis: ", ecg_diagnosis, "echo_diagnosis: ", echo_diagnosis)
        
        final_diagnosis = MODEL_LABELS['integrated'][integ_diagnose(rf_diagnosis, ecg_diagnosis, echo_diagnosis)]
        # final_diagnosis = MODEL_LABELS['integrated'][1] if rf_diagnosis == MODEL_LABELS
        # + ecg_diagnosis + echo_diagnosis # frontend already checks that at least one model is checked so this will never be null or ''
        print("final_diagnosis: ", final_diagnosis)


        # Create the DoctorPatientFiles model entry
        modelsUsed = {
            'Tabular': request.data.get('Tabular'),
            'ECG': request.data.get('ECG'),
            'Echo': request.data.get('Echo')
        }
        print("modelsUsed: ", modelsUsed)
        data = {
            'doctor': request.data.get('doctor'),
            'patient': request.data.get('patient'),
            'final_diagnosis': final_diagnosis
            }
        if(modelsUsed['Tabular'] == 'true'):
            data.update({
                'age': request.data.get('age'),
                'sex': request.data.get('sex'),
                'cp': request.data.get('cp'),
                'trestbps': request.data.get('trestbps'),
                'chol': request.data.get('chol'),
                'fbs': request.data.get('fbs'),
                'restecg': request.data.get('restecg'),
                'thalach': request.data.get('thalach'),
                'exang': request.data.get('exang'),
                'oldpeak': request.data.get('oldpeak'),
                'slope': request.data.get('slope'),
                'ca': request.data.get('ca'),
                'thal': request.data.get('thal'),
                'rf_diagnosis': request.data.get('rf_diagnosis')

            })
        else:
            data.update({
                'age': None,
                'sex': None,
                'cp': None,
                'trestbps': None,
                'chol': None,
                'fbs': None,
                'restecg': None,
                'thalach': None,
                'exang': None,
                'oldpeak': None,
                'slope': None,
                'ca': None,
                'thal': None,
                'rf_diagnosis': None

            })
        if(modelsUsed['ECG'] == 'true'):
            data.update({
                'dat_file': request.data.get('dat_file'),
                'hea_file': request.data.get('hea_file'),
                'xyz_file': request.data.get('xyz_file'),
                'ecg_diagnosis': request.data.get('ecg_diagnosis')

            })
            # Attach the local files to the data dictionary
            try:
                with open(request.data.get('image_ii'), 'rb') as f:
                    data['image_ii'] = ContentFile(f.read(), request.data.get('dat_file').name + "_ii_model.png")

                with open(request.data.get('image_v6'), 'rb') as f:
                    data['image_v6'] = ContentFile(f.read(), request.data.get('dat_file').name + "_v6_model.png")

                with open(request.data.get('image_vz'), 'rb') as f:
                    data['image_vz'] = ContentFile(f.read(), request.data.get('dat_file').name + "_vz_model.png")
            except Exception as e:
                print(f"Error reading files: {e}")
        
        if(modelsUsed['Echo'] == 'true'):
            data.update({
                # 'video': request.data.get('video'),
                'echo_diagnosis': request.data.get('echo_diagnosis'),
                'prognosis': request.data.get('prognosis'),

            })
            print("YEAH echo_diagnosis = ", request.data.get('echo_diagnosis'))
            print("YEAH2 echo_diagnosis = ", data['echo_diagnosis'])
            try:
                print("kindly:", request.data.get('video'))
                video_path = request.data.get('video')

                # Extract the file name from the file path
                video_name = os.path.basename(video_path)

                with open(video_path, 'rb') as f:
                    data['video'] = ContentFile(f.read(), video_name + "_model.avi")

            except Exception as e:
                print(f"Error reading files: {e}")

        
        print("data...", data)
        print('\n')
        # print("request.data...", request.data)
        # print('\n')

        serializer = DoctorPatientFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)