from django.contrib import messages
from django.shortcuts import render, redirect

from cough_app.forms import LoginForm, hospitalform
from cough_app.models import Doctor, hospital, Login


def adminhome(request):
    return render(request, 'admintemp/admin.html')


def AddHospital(request):
    loginform = LoginForm()
    hsptlfrm = hospitalform()
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        hsptlfrm = hospitalform(request.POST)
        if loginform.is_valid() and hsptlfrm.is_valid():
            user = loginform.save(commit=False)
            user.is_hospital = True
            user.save()
            hospital = hsptlfrm.save(commit=False)
            hospital.user = user
            hospital.save()
            messages.info(request, "successfully registered")
            return redirect('ViewHospital')
    return render(request, 'admintemp/AddHospital.html', {'loginform': loginform, 'hsptlfrm': hsptlfrm})


def ViewHospital(request):
    Hspt = hospital.objects.all()
    return render(request, 'admintemp/ViewHospital.html', {'Hspt': Hspt})


def ViewDoctor(request):
    Doc = Doctor.objects.all()
    return render(request, 'admintemp/ViewDoctor.html', {'Doc': Doc})


def hospitalhome(request):
    return render(request, 'hospitaltemp/hospitalhome.html')


def user_view_admin(request):
    log = Login.objects.filter(is_user=True)
    return render(request, 'admintemp/user_view.html', {'log': log})
