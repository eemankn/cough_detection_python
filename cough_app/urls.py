from django.urls import path

from cough_app import views, adminviews, apiviews, hospitalviews

urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login_view,name='login'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('adminhome', adminviews.adminhome, name='adminhome'),
    path('AddHospital',adminviews.AddHospital,name='AddHospital'),
    path('ViewDoctor', adminviews.ViewDoctor, name='ViewDoctor'),
    path('ViewHospital', adminviews.ViewHospital, name='ViewHospital'),
    path('user_view_admin', adminviews.user_view_admin, name='user_view_admin'),

    path('hospitalhome',hospitalviews.hospitalhome,name='hospitalhome'),
    path('hospitalProfile',hospitalviews.hospitalProfile,name='hospitalProfile'),
    path('updatehospital',hospitalviews.updateHospital,name='updatehospital'),
    path('AddDoctor', hospitalviews.AddDoctor, name='AddDoctor'),
    path('DoctorView', hospitalviews.DoctorView, name='DoctorView'),
    path('Schedule',hospitalviews.schedule_add,name='Schedule'),
    path('ViewSchedule',hospitalviews.Viewschedule,name='ViewSchedule'),


    path('Doctorhome',views.doctorhome,name='Doctorhome'),
    path('profile',views.ViewProfile,name='profile'),
    path('updateDoctor/<int:id>',views.updateDoctor,name='updateDoctor'),
    path('chatwithUser',views.chat_list_d,name='chatwithUser'),
    path('chat_page_d/<int:id>',views.chat_page_d,name='chat_page_d'),

    path('user_register',views.user_register,name='user_register'),
    path('prescription_add',views.prescription_add,name='prescription_add'),
    path('ViewPrescription',views.ViewPrescription,name='ViewPrescription'),



    path('login_view_api/',apiviews.login_view_api,name='login_view_api'),
    path('user_reg',apiviews.user_reg,name='user_reg'),

    path('doctor_list',apiviews.doctor_list,name='doctor_list'),
    path('schedule_list', apiviews.schedule_list, name='schedule_list'),
    path('booking_api', apiviews.booking_api.as_view(), name='booking_api'),
    path('prescription_api',apiviews.prescription_api,name='prescription_api'),
    path('home2', apiviews.home2, name='home2'),

]
