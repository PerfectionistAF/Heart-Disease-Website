from django.urls import path
from .views import RegisterView, LoginView , PatientListCreateView, PatientDetailView, DoctorPatientFileListCreateView, DoctorPatientFileDetailView, Risk_Factors_Model_Predict, ECGFileUploadView, EchoFileUploadView, DoctorPatientFileView#ECG_Model_Predict


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('doctor-patient-files/', DoctorPatientFileListCreateView.as_view(), name='doctor-patient-file-list-create'),
    path('doctor-patient-files/<int:pk>/', DoctorPatientFileDetailView.as_view(), name='doctor-patient-file-detail'),

    path('risk-factors-predict/', Risk_Factors_Model_Predict.as_view(), name = 'predict'), # post request sends rf attributes, receives http response dict containing rf prediction
    # path('ecg-predict/', ECG_Model_Predict.as_view(), name = 'ecg-predict'),
    path('upload/', ECGFileUploadView.as_view(), name='ecg-file-upload'), #  step 1) post request sends ecg dat hea and xyz files, receives http response containing ecg prediction and processed base64 images
    path('upload-echo/', EchoFileUploadView.as_view(), name='ecg-file-upload'),
    path('doctor-patient-file-upload/', DoctorPatientFileView.as_view(), name='doctor-patient-file-upload'), # step 2) post request sends ecg base64 images along with all form data and diagnosis from previous steps. 
    
]
