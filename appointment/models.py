from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date, datetime, time, timedelta
# Create your models here.

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 

    class Meta:
        db_table = "users"
        
@receiver(post_save, sender=User)
def create_user_usermodel(sender, instance, created, **kwargs):
    if created:
        UserModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_model(sender, instance, **kwargs):
    instance.usermodel.save()



class Doctor(models.Model):
    doctor_name = models.CharField(max_length=128)
    specialist = models.CharField(max_length=512)
    experince = models.CharField(max_length=512)
    charges = models.CharField(max_length=512)
    avatar = models.ImageField()

    def __str__(self):
        return self.doctor_name

times = []
for i in range(0, 24*4):
    times.append((datetime.combine(date.today(), time()) + timedelta(minutes=15) * i).time())
TIMES_SLOT = [("","---------")]+[( choice.strftime("%H:%M:%S"), choice.strftime("%I:%M %p").lstrip('0') ) for choice in times]

class Timings(models.Model):
    slots = models.CharField(max_length=50, unique=True, choices=TIMES_SLOT)

    def __str__(self):
        dt = datetime.strptime(self.slots,"%H:%M:%S")
        return dt.strftime("%I:%M %p")

class DoctorTimeSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    my_slot = models.ManyToManyField(Timings)

    def slots_time(self):
        return ", ".join([datetime.strptime(a.slots,"%H:%M:%S").strftime("%I:%M %p") for a in self.my_slot.all()])

class MyAppointments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    timing = models.ForeignKey(Timings, on_delete=models.CASCADE)
    


    
