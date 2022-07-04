import random

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cough_app.models import Doctor, schedule, Appoinment, Prescription, Cough
from cough_app.serializer import DoctorSerializer, ScheduleSerializer, bookingSerializer, prescriptionSerializer, \
    CoughSerializer

from cough_app.forms import userform
import numpy as np
from tensorflow.keras.models import load_model
import librosa
import librosa.display



@csrf_exempt
def login_view_api(request):

    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('hi',username)
            if user.is_user:
                type = 'user'
            elif user.is_doctor:
                type = 'doctor'
                result = user.is_authenticated
    try:
        result = user.is_authenticated
        data = {
            'status':True,
            'result': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'type': type
            }
        }
    except:
        data = {
            'status': False
        }
    return JsonResponse(data, safe=False)




# @api_view(['GET', 'POST'])
# def userdetails(request):
#     if request.method == 'GET':
#         userdetails = user.objects.all()
#         serializer = 'UserSerializer'(User, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def user_reg(request):
    result_data = None
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.is_active = True
            form.is_user = True
            form.save()
            result_data = True
    try:
        if result_data:
            data = {'result': True}
        else:
            print(list(form.errors))
            error_data = form.errors
            error_dict = {}
            for i in list(form.errors):
                error_dict[i] = error_data[i][0]

            data = {
                'result':False,
                'errors':error_dict
            }
    except:
        data = {
            'result':False
        }
    return JsonResponse(data, safe=False)

@api_view(['GET','POST'])
def doctor_list(request):

    if request.method =='GET':
        doctor = Doctor.objects.all()
        serializer=DoctorSerializer(doctor,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def schedule_list(request):

    if request.method =='GET':
        Schedule = schedule.objects.all()
        serializer=ScheduleSerializer(Schedule,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class booking_api(generics.ListCreateAPIView):
    queryset = Appoinment.objects.all()
    serializer_class = bookingSerializer

# class prescription_api(generics.ListCreateAPIView):
#     queryset = Prescription.objects.all()
#     serializer_class = prescriptionSerializer

@api_view(['GET','POST'])
def prescription_api(request):

    if request.method =='GET':
        p = Prescription.objects.all()
        serializer=prescriptionSerializer(p,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = prescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





def extract_feature(audio_path, offset):
   y, sr = librosa.load(audio_path, offset=offset, duration=3)
   S = librosa.feature.melspectrogram(
   y, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
   mfccs = librosa.feature.mfcc(S=librosa.power_to_db(S), n_mfcc=40)
   # mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
   return mfccs


class cough_api(generics.ListCreateAPIView):
    queryset = Cough.objects.all()
    serializer_class = CoughSerializer

@api_view(['GET','POST'])
def home2(request):
    if request.method == 'POST':
        cough = Cough.objects.filter(cough=request.user)
        serializer = CoughSerializer(cough,many=True)
        return Response(serializer.data)
    if __name__ == "__main__":
        # load model
        model = load_model("cough_classifier3.h5")
        # File to be classified
        # classify_file = "125_Positive_male_51 - Copy - Copy.wav"
        # classify_file = sys.argv[1]
        x_test = []
        x_test.append(extract_feature(Cough, 0.5))
        x_test = np.asarray(x_test)
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
        pred = model.predict(x_test, verbose=1)
        # print(pred)

        pred_class = model.predict(x_test)
        if pred[0][1] >= 0.7:
            prediction="PNEUMONIC PATIENT"
        else:
            prediction="NEGATIVE"
        print(prediction)
        print("confidence:", pred[0][1])
        return Response(prediction.data, status=status.HTTP_201_CREATED)
        return Response(prediction.errors, status=status.HTTP_400_BAD_REQUEST)



