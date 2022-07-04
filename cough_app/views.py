from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError

from cough_app.forms import doctorform, scheduleform, LoginForm, hospitalform, userform, prescriptionform
from cough_app.models import Doctor, hospital, schedule, Login, Chat, Prescription


def home(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminhome')
            elif user.is_hospital:
                return redirect('hospitalhome')
            elif user.is_doctor:
                return redirect('Doctorhome')
        else:
            messages.info(request, 'Invalid username,password')
    return render(request, 'login.html')


# def ViewDoctor(request):
#     Doc = Doctor.objects.all()
#     return render(request, 'hospitaltemp/DoctorView.html', {'Doc': Doc})


def ViewHospital(request):
    hsptl = hospital.objects.get()
    return render(request, 'ViewHospital.html', {'hsptl': hsptl})


def doctorhome(request):
    return render(request, 'doctortemp/doctorhome.html')


def ViewProfile(request):
    u=request.user
    doctor = Doctor.objects.get(user_id=u)
    return render(request, 'doctortemp/profile.html', {'doctor': doctor})

def updateDoctor(request,id):
    d = Doctor.objects.get(id=id)
    l = Login.objects.get(doctor=d)
    if request.method == 'POST':
        form = doctorform(request.POST or None,instance=d)
        user_form = LoginForm(request.POST or None,instance=l)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.info(request,'Schedule updated')
            return redirect('profile')
    else:
        form = doctorform(instance=d)
        user_form = LoginForm(instance=l)
    return render(request,'doctortemp/UpdateDoctor.html',{'form':form, 'user_form':user_form})

def user_register(request):
    if request.method=='POST':
        form = userform(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.is_user = True
    else:
        form = userform()
    return render(request,'user_register.html',{'form':form})

# def take_appoinment(request,id):
#     s = schedule.objects.get(id=id)
#     u = User.objects.get(user=request.user)
#     appoinment = Appoinment.objects.filter(user=u,schedule=s)
#     if appoinment.exists():
#         messages.info(request,'you have already requested appoinment for this schedule')
#         return  request('schedule')
#     else:
#         if request.method == 'POST'
#             obj = Appoinment()
#             obj.user = u
#             obj.schedule = s
#             obj.save()
#             messages.info(request,'Appoinment Booked')
#             return redirect('appoinment_view')
#         return render(request,'userpage/')

# @login_required
# def chat_list(request):
#     list = Login.objects.filter(is_user=True)
#     return render(request, 'customer/ChatwithUser.html', {'data': list})
#
# @login_required
# def chat_page(request):
#     # user_data = CustomUser.objects.get(id=id)
#
#     users_view = Login.objects.filter(is_user=True)[0]
#     c_user = Login.objects.get(id=request.user.id)
#
#     final = Chat.objects.all()
#     cus_chat = Chat.objects.filter(receiver=request.user)
#     for i in cus_chat:
#         i.c_seen = True
#         i.save()
#     request.session['chat'] = 0
#
#     # print(final)
#     if request.method == 'POST' or request.FILES:
#
#         try:
#             msg = request.POST.get('message')
#             img = request.FILES['img']
#             Chat.objects.create(message=msg, sender=request.user, receiver=users_view, image=img).save()
#             return redirect('chat_page', )
#         except MultiValueDictKeyError:
#             Chat.objects.create(message=msg, sender=request.user, receiver=users_view).save()
#             return redirect('chat_page')
#
#     current_user = request.user
#     # u_id2 = user_data
#
#     context = {
#
#         'current_user': current_user,
#         'final': final,
#
#     }
#     return render(request, 'customer/ChatwithUser.html', context)



def chat_list_d(request):
    list = Login.objects.filter(is_user=True)
    return render(request, 'doctortemp/ChatwithUser.html', {'data': list})


def chat_page_d(request, id):
    user_data = Login.objects.get(id=id)

    # users_view = CustomUser.objects.filter(is_customer=True)
    # c_user = CustomUser.objects.get(id=request.user.id)
    # data = Chat.objects.filter(receiver__in=[user_data.id, c_user.id],
    #                            sender__in=[request.user.id, user_data.id])
    # data2 = Chat.objects.filter(receiver=user_data, sender=request.user.id)
    # data1 = Chat.objects.filter(receiver=c_user, sender=id)

    final = Chat.objects.all()

    if request.method == 'POST' or request.FILES:
        # if request.method == 'POST' or request.FILES:

        try:
            msg = request.POST.get('message')
            img = request.FILES['img']
            Chat.objects.create(message=msg, sender=request.user, receiver=user_data, image=img).save()
            return redirect('chat_page_d', id)
        except MultiValueDictKeyError:
            Chat.objects.create(message=msg, sender=request.user, receiver=user_data).save()
            return redirect('chat_page_d', id)

    u_id1 = request.user
    customer = user_data

    context = {

        'current_user': user_data,

        'customer': customer,
        'xx': u_id1,

        'final': final,

    }
    return render(request, 'doctortemp/ChatwithUser.html', context)

def prescription_add(request):
    form = prescriptionform()
    if request.method == 'POST':
        form =prescriptionform (request.POST,request.FILES)
        if form.is_valid():
            form = form.save()
        return  redirect('ViewPrescription')
    return  render(request,'doctortemp/PrescriptionAdd.html',{'form':form})

def ViewPrescription(request):
    pres = Doctor.objects.all()
    return render(request, 'doctortemp/ViewPrescription.html', {'pres': pres})
