from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class Patient(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor', on_delete=models.CASCADE)

    name = models.CharField(max_length=250)
    birthdate = models.DateTimeField()
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient: {self.name}"


class DoctorPatientFile(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor_files', on_delete=models.CASCADE)
    patient = models.ForeignKey("users.Patient", related_name='patient_files', on_delete=models.CASCADE)
    
    # reference_number = models.CharField(max_length=100, unique=True) # this is different to django's auto-generated id
    
    age = models.IntegerField(verbose_name='Age (years)', blank=True, null=True)
    sex = models.IntegerField(verbose_name='Sex', choices=[(1, 'Male'), (0, 'Female')], default=1, blank=True, null=True)
    cp = models.IntegerField(verbose_name='Chest Pain Type', choices=[(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-Anginal Pain'), (4, 'Asymptomatic')], blank=True, null=True)  
    trestbps = models.IntegerField(verbose_name='Resting Blood Pressure (mm Hg) on admission to the hospital', blank=True, null=True)
    chol = models.FloatField(verbose_name='Total Serum Cholesterol (mg/dl)', blank=True, null=True)
    fbs = models.IntegerField(verbose_name='Fasting Blood Sugar > 120 mg/dl?', choices=[(1, 'True'), (0, 'False')], default=1, blank=True, null=True)
    restecg = models.IntegerField(verbose_name='Resting Electrocardiographic Results', choices=[(0, 'Normal'), (1, 'Abnormal - ST-T wave'), (2, 'Abnormal - Left Ventricular Hypertrophy')], blank=True, null=True)
    thalach = models.IntegerField(verbose_name='Maximum Heart Rate Achieved', blank=True, null=True)
    exang = models.IntegerField(verbose_name='Exercise Induced Angina?', choices=[(1, 'Yes'), (0, 'No')], default=0, blank=True, null=True)
    oldpeak = models.FloatField(verbose_name='ST Depression Induced by Exercise Relative to Rest', blank=True, null=True)
    slope = models.IntegerField(verbose_name='Slope of the Peak Exercise ST Segment', choices=[(1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')], blank=True, null=True)
    ca = models.FloatField(verbose_name='Number of Major Vessels (0-3) Colored by Fluoroscopy', blank=True, null=True)
    thal = models.IntegerField(verbose_name='Thalassemia', choices=[(3, 'Normal'), (6, 'Fixed Defect'), (7, 'Reversible Defect')], blank=True, null=True)

    rf_diagnosis = models.CharField(max_length=255, blank=True, null=True)  # CharField for shorter entries



    dat_file = models.FileField(verbose_name="ECG_dat", upload_to='ecg/input/', blank=True, null=True)
    hea_file = models.FileField(verbose_name="ECG_hea", upload_to='ecg/input/', blank=True, null=True)
    xyz_file = models.FileField(verbose_name="ECG_xyz", upload_to='ecg/input/', blank=True, null=True)
    image_ii = models.ImageField(verbose_name="ECG_ii", upload_to='ecg/output/', blank=True, null=True) # show the images and dat_file filename to user in frontend
    image_v6 = models.ImageField(verbose_name="ECG_v6", upload_to='ecg/output/', blank=True, null=True)
    image_vz = models.ImageField(verbose_name="ECG_vz)", upload_to='ecg/output/', blank=True, null=True)
    
    ecg_diagnosis = models.CharField(max_length=255, blank=True, null=True)



    video = models.FileField(verbose_name="Echocardiogram", upload_to='videos/', blank=True, null=True)
    echo_diagnosis = models.CharField(max_length=255, blank=True, null=True)



    prognosis = models.TextField(blank=True, null=True) # TextField for longer entries

    final_diagnosis = models.CharField(max_length=255, blank=True, null=True)  # CharField for shorter entries



    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doctor-Patient File: {self.patient.name}"
    


# https://corgibytes.com/blog/2022/06/14/model-relationships-django-rest-framework/
#     There are three major kinds of relationship between database entries:

# One-to-many (a.k.a. a ForeignKey): for example, a Pizza is associated with exactly one Order, but an Order can have more than one Pizza.
# One-to-one: for example, a Pizza has exactly one Box, and each Box belongs to one Pizza.
# Many-to-many: for example, a Pizza can have more than one Topping, and a single Topping can be on more than one Pizza.

