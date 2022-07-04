from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput, TimeInput

from cough_app.models import Login, hospital, Doctor, schedule, Prescription


class DateInput(forms.TimeInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class LoginForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')


class userform(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Login
        fields = ('username', 'password1', 'password2', 'name', 'age', 'address', 'height', 'weight', 'phone_number','email')


class hospitalform(forms.ModelForm):
    class Meta:
        model = hospital
        fields = ('name', 'address', 'location', 'email', 'phone_number')


class doctorform(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            'name', 'address', 'hospital_name', 'qualification', 'speacialisation', 'experience', 'email',
            'phone_number',
            'image')


class scheduleform(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput)
    end_time = forms.TimeField(widget=TimeInput)


    class Meta:
        model = schedule
        fields = ('date', 'start_time', 'end_time','doctor')


class prescriptionform(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Prescription
        fields = ('date','prescription')







# class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = ImageUpload
#         fields= (
#             'title',
#             'images'
#         )