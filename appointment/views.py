from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointment.forms import *
from appointment.models import *
from appointment.functions import handle_uploaded_file
from .functions import *
from django.db.models import Q



from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

def dashboard(request):    
    if 'user' in request.session:
        data = User.objects.get(id=request.session['user']['user_id'])
        
        # print(data[0].name)
        context = {
            'data' : data,
        }        
       
        return redirect('/profile/')
    else:
        return redirect("/login/")

def UserLogin(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            var = request.POST.get('email')
            pwd = request.POST.get('password')            
            if '@' in var :         
                check = authenticate(email=var, password=pwd)
                n = 'Email '              
            else:

                check = authenticate(username=var, password=pwd)
                n = 'Username '          
            
            if check and check != None:
                if check_password(pwd,check.password):
                    login(request, check)
                    request.session['user'] = { 'email' : check.email, 'user_id' : check.id }
                   
                    return redirect("/")
                else:
                    messages.error(request, n+" and password is incorrect.")
                    return redirect("/login/")
                    
            else:
                messages.error(request, "User doesn't exist. or you are banned")
                return redirect("/login/")            

    else:
        form = LoginForm()
    context = {
        'form':form
    }

    return render(request, 'login.html', context)

def UserRegister(request):
    if request.method == 'POST':
        form = regForm(request.POST)
        if form.is_valid():            
            password = make_password(request.POST['password'])
            uname = request.POST['uname']
            email = request.POST['email']
            name = request.POST['name']       
            regist = User.objects.create(username=uname, email=email,
                     first_name=name, password=password, is_active=1)  
            
            

            if regist :
                messages.success(request, 'Thank you for register with us')
                return redirect("/login/")
            else :
                messages.error(request, 'Something went wrong.')
                return redirect("/register/")
    else:
        form = regForm()
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)

def GetProfile(request):
    print(request.session)
    if 'user' in request.session :        
        data = User.objects.get(pk=request.session['user']['user_id'])
        context = {
            'data' : data,
            
        }
        return render(request, 'profile.html', context)
    else:
        return redirect("/login/")


        return redirect("/login/")

def ChangeStatus(request, status, user_id=None):
    if 'user' in request.session and user_id != None:
        if request.session['user']['role'] == 'admin':
            data = UserModel.objects.only("user_id","status").get(user_id=user_id)
            if status == 1:
                data.status = 0
            else:
                print(user_id)
                print(status)        
                data.status = 1
            data.save()        
            return redirect("/")
        else:
            return redirect("/login/")
    else:
        return redirect("/login/")

def logout(request):
    request.session.flush()
    return redirect('/login/')

@login_required
def doctorsList(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', locals())

@login_required
def doctorsDetails(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        doctorTimings = DoctorTimeSchedule.objects.get(doctor=doctor_id)
        timings = doctorTimings.my_slot.all()
    except:
        return redirect('/doctors/')
    return render (request, 'single_doctor.html', locals())

@login_required
def doctorsAppoint(request, doctor_id, time_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        timings = Timings.objects.get(id=time_id)
        appoint = MyAppointments()
        appoint.user_id = request.user
        appoint.doctor_id = doctor
        appoint.timing = timings
        appoint.save()
    except Doctor.DoesNotExist:
        messages.ERROR(request, 'Doctor not valid')
        return redirect('/doctors/')
    except Timings.DoesNotExist:
        messages.ERROR(request, 'Invalid timing')
        return redirect('/doctor/'+str(doctor_id))
    messages.success(request, 'Your Appointment is booked')
    return redirect('/my-appointments')

@login_required
def myAppointment(request):
    
    appointments = MyAppointments.objects.filter(user_id=request.user)
    if not appointments:
        messages.ERROR(request, 'You have no appointment')
        return redirect('/profile')
    return render(request, 'myappointment.html', locals())