from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(User, Role,Accept,Requesttutor)
class ViewAdmin(ImportExportModelAdmin):
    pass