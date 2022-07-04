from django.contrib import messages
from django.shortcuts import render, redirect

from cough_app.forms import LoginForm, doctorform, scheduleform, hospitalform
from cough_app.models import hospital, schedule, Doctor, Login


def hospitalhome(request):
    return render(request, 'hospitaltemp/hospitalhome.html')


def AddDoctor(request):
    loginform = LoginForm()
    doctorfrm = doctorform()
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        doctorfrm = doctorform(request.POST, request.FILES)
        if loginform.is_valid() and doctorfrm.is_valid():
            user = loginform.save(commit=False)
            user.is_doctor = True
            user.save()
            doctor = doctorfrm.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.info(request, "successfully registered")
            return redirect('ViewDoctor')
    return render(request, 'hospitaltemp/AddDoctor.html', {'loginform': loginform, 'doctorfrm': doctorfrm})


def DoctorView(request):
    D = Doctor.objects.all()
    return render(request, 'hospitaltemp/DoctorView.html',{'D':D})


def schedule_add(request):
    form = scheduleform()
    if request.method == 'POST':
        form = scheduleform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = hospital.objects.get(user=request.user)
            form.save()
            messages.info(request, 'Schedule added Successful')
            return redirect('ViewSchedule')
    return render(request, 'hospitaltemp/schedule.html', {'form': form})


def Viewschedule(request):
    u = hospital.objects.get(user=request.user)
    s = schedule.objects.filter(user=u)
    context = {
        'schedule': s
    }
    return render(request, 'hospitaltemp/ViewSchedule.html', context)

def hospitalProfile(request):
    u=request.user
    hospitalprofile = hospital.objects.get(user_id=u)
    return render(request, 'hospitaltemp/profileView.html', {'hospitalprofile': hospitalprofile})

def updateHospital(request,id):
    h = hospital.objects.get(id=id)
    l = Login.objects.get(Hospital=h)
    if request.method == 'POST':
        form = hospitalform(request.POST or None,instance=h)
        user_form = LoginForm(request.POST or None,instance=l)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.info(request,'Schedule updated')
            return redirect('profile')
    else:
        form = doctorform(instance=d)
        user_form = LoginForm(instance=l)
    return render(request,'hospitaltemp/UpdateHospital.html',{'form':form, 'user_form':user_form})