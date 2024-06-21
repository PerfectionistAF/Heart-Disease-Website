from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import User, Patient, DoctorPatientFile
from .serializers import UserSerializer, LoginSerializer, PatientSerializer, DoctorPatientFileSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PatientFilter, DoctorPatientFileFilter
from .apps import RiskFactorsPredictionConfig
import pandas as pd


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
    ordering_fields = ['doctor', 'patient', 'diagnosis', 'prognosis', 'created_at']
    ordering = ['created_at']

class DoctorPatientFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorPatientFile.objects.all()
    serializer_class = DoctorPatientFileSerializer









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
        target_map = {0: '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)', 1: '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'}
        y_pred = y_pred.map(target_map).to_numpy()
        response_dict = {"Risk Factors Prediction": y_pred[0]}



        return Response(response_dict, status=200)