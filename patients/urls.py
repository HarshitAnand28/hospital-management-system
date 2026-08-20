from django.urls import path
from patients import views

urlpatterns=[
    path('CareBridge/', views.public_site, name="CareBridge"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('doctorDetails/', views.doctorDetails, name="doctorDetails"),
    path('searchDoctorDetails/Service/', views.searchDoctorDetails, name="searchDoctorDetails"),
    path('deleteDoctorDetails/<doctor_ID>/Delete/', views.deleteDoctorDetails, name='deleteDoctorDetails'),
    path('updateDoctorDetails/<doctor_ID>/Update/', views.updateDoctorDetails, name='updateDoctorDetails'),
    path('patientDetails/', views.patientDetails, name="patientDetails"),
    path('searchPatientsDetails/Service/', views.searchPatientsDetails, name="searchPatientsDetails"),
    path('deletePatientDetails/<patient_ID>/Delete/', views.deletePatientDetails, name='deletePatientDetails'),
    path('updatePatientDetails/<patient_ID>/Update/', views.updatePatientDetails, name='updatePatientDetails'),
    path('appointmentDetails/', views.appointmentDetails, name="appointmentDetails"),
    path('searchAppointmentDetails/Service/', views.searchAppointmentDetails, name='searchAppointmentDetails')
]