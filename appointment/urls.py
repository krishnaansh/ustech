from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


app_name = 'mysites'

urlpatterns = [    
    path('', dashboard, name='dashboard'),   
    path('login/', UserLogin, name="userLogin"),
    path('register/', UserRegister, name="register"),
    path('profile/', GetProfile, name="profile"),
    path('user/status/<int:status>/<int:user_id>', ChangeStatus, name="change-status"),
    path('user/logout/', logout, name="user-logout"),
    path('doctors/', doctorsList, name='doctors-list'),
    path('doctor/<int:doctor_id>', doctorsDetails, name='single-doctor'),
    path('doctor/appointment/<int:doctor_id>/<int:time_id>', doctorsAppoint, name='appointment-doctor'),
    path('my-appointments', myAppointment, name='appointment')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)