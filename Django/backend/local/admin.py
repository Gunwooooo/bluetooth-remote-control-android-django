from django.contrib import admin
from .models import HospitalInfo, PharmacyInfo
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

class HospitalInfoadmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(HospitalInfo, HospitalInfoadmin)

class PharmacyInfoadmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(PharmacyInfo, PharmacyInfoadmin)