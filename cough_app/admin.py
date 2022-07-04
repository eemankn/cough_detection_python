from django.contrib import admin

# Register your models here.
from cough_app import models

admin.site.register(models.Login)
admin.site.register(models.hospital)
admin.site.register(models.Doctor)