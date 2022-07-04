from rest_framework import serializers

from cough_app.models import Doctor, schedule, Appoinment, Prescription, Cough


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=['id','name','hospital_name','speacialisation','image']

class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model=schedule
        fields=['user','date','start_time','end_time','doctor']

class bookingSerializer(serializers.ModelSerializer):
            class Meta:
                model = Appoinment
                fields = ['user', 'Schedule']

class prescriptionSerializer(serializers.ModelSerializer):
            class Meta:
                model = Prescription
                fields = ['date','prescription']

class CoughSerializer(serializers.ModelSerializer):
            class Meta:
                model = Cough
                fields = ['cough']

