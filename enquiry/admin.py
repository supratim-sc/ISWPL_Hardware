from django.contrib import admin

from .models import Enquiry, EnquiryType, TeleCaller, ReferenceType

# Registering sites
class CustomEnquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'enquiry_type', 'service_description', 'reference_type']
    list_filter = ['enquiry_type', 'reference_type', 'tele_caller_name']

admin.site.register(Enquiry, CustomEnquiryAdmin)


class CustomEnquiryTypeAdmin(admin.ModelAdmin):
    list_display = ['enquiry_type', 'created_by', 'created_at', 'updated_at']
    list_filter = ['created_by']

admin.site.register(EnquiryType, CustomEnquiryTypeAdmin)


class CustomTeleCallerAdmin(admin.ModelAdmin):
    list_display = ['tele_caller_name', 'created_by', 'created_at', 'updated_at']
    list_filter = ['created_by']

admin.site.register(TeleCaller, CustomTeleCallerAdmin)


class CustomReferenceTypeAdmin(admin.ModelAdmin):
    list_display = ['reference_type', 'created_by', 'created_at', 'updated_at']
    list_filter = ['created_by']

admin.site.register(ReferenceType, CustomReferenceTypeAdmin)
