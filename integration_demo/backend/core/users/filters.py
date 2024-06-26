import django_filters
from .models import Patient, DoctorPatientFile, User
from django.conf import settings

class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    doctor = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Patient
        fields = ['name', 'doctor', 'created_at']

class DoctorPatientFileFilter(django_filters.FilterSet):
    doctor = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    patient = django_filters.ModelChoiceFilter(queryset=Patient.objects.all())
    final_diagnosis = django_filters.CharFilter(lookup_expr='icontains')
    prognosis = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = DoctorPatientFile
        fields = ['doctor', 'patient', 'final_diagnosis', 'prognosis', 'created_at']
