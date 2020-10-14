from django.contrib import admin
from appointment.models import DoctorTimeSchedule, Doctor, Timings
# Register your models here.

@admin.register(Doctor)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'specialist')

@admin.register(DoctorTimeSchedule)
class DoctorTimeScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ('my_slot',)
    list_display = ('doctor', 'slots_time')

@admin.register(Timings)
class TimingAdmin(admin.ModelAdmin):
    list_display = ('slots',)