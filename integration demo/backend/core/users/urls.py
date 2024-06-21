from django.urls import path
from .views import RegisterView, LoginView , PatientListCreateView, PatientDetailView, DoctorPatientFileListCreateView, DoctorPatientFileDetailView, Risk_Factors_Model_Predict

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('doctor-patient-files/', DoctorPatientFileListCreateView.as_view(), name='doctor-patient-file-list-create'),
    path('doctor-patient-files/<int:pk>/', DoctorPatientFileDetailView.as_view(), name='doctor-patient-file-detail'),

    path('risk-factors-predict/', Risk_Factors_Model_Predict.as_view(), name = 'predict'),

]
