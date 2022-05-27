from django.contrib import admin
from .models import Employee


class EmployeeManager(admin.ModelAdmin):
    list_display = ['name', 'surname', 'image', 'profession']


admin.site.register(Employee, EmployeeManager)