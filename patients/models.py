from django.db import models

# Create your models here.

class DoctorReg(models.Model):
    doctor_ID = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    cont_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254, null=True, blank=True)
    gender = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, null=True, blank=True)
    id_type = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20)
    photo = models.FileField(upload_to='doctor_photo/', null=True, blank=True)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pin = models.CharField(max_length=6)
    address = models.TextField(max_length=100)

class PatientReg(models.Model):
    patient_ID = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    cont_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254, null=True, blank=True)
    gender = models.CharField(max_length=100)
    id_type = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20)
    photo = models.FileField(upload_to='patient_photo/', null=True)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pin = models.CharField(max_length=6)
    address = models.TextField(max_length=100)

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorReg, to_field="doctor_ID", on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(PatientReg, to_field="patient_ID", on_delete=models.CASCADE, null=True, blank=True)
    appointment_ID = models.CharField(max_length=100, unique=True)
    appointment_Date = models.DateField()
    appointment_Time = models.TimeField()
    status = models.CharField(max_length=50)

class Address(models.Model):
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)