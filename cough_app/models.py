from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Login(AbstractUser):
    is_hospital = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    name = models.CharField(max_length=100,null=True)
    age= models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=100,null=True)
    height = models.CharField(max_length=100,null=True)
    weight = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=100,null=True)

class hospital(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='hospital')
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    location = models.CharField(max_length=10)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='doctor')
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    hospital_name = models.CharField(max_length=50)
    # department = models.CharField(max_length=10)
    qualification = models.CharField(max_length=100)
    speacialisation = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    image=models.ImageField(upload_to='photo')

    def __str__(self):
        return self.name

class schedule(models.Model):
    user = models.ForeignKey(hospital,on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Appoinment(models.Model):
    user = models.ForeignKey(Login,on_delete=models.CASCADE,related_name='appointment')
    Schedule = models.ForeignKey(schedule,on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

class Prescription(models.Model):
    user = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,null=True)
    date = models.DateField()
    prescription = models.FileField(upload_to='File',null='True')

class Chat(models.Model):
    sender = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='chat_sender')
    receiver = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='chat_receiver')
    message = models.CharField(max_length=200)
    image = models.ImageField(upload_to='suggestion', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    c_seen = models.BooleanField(default=False)
    d_seen = models.BooleanField(default=False)


class Cough(models.Model):
    user = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,null=True)
    cough = models.FileField(upload_to='File',null='True')
