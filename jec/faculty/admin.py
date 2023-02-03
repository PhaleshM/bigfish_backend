from django.contrib import admin
from .models import Faculty
from user.forms import PastCustomDatePickerWidget
from django.db import models

class FacultyAdmin(admin.ModelAdmin):
    list_display=['name','department','designation','dob','doa','exp','regular']
    formfield_overrides={
        models.DateField:{'widget':PastCustomDatePickerWidget},
    }
# Register your models here.
admin.site.register(Faculty,FacultyAdmin)