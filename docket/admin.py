from django.contrib import admin
from .models import Docket, DocketUpdateLog

# Register your models here.
# Define the Inline for DocketUpdateLog
class DocketUpdateLogInline(admin.TabularInline):
    model = DocketUpdateLog
    extra = 0  # No extra blank forms
    readonly_fields = ('updated_at',)  # Optional
    fields = ('assigned_engineer', 'updated_by', 'status', 'updated_at')  # Customize as needed


class DocketAdmin(admin.ModelAdmin):
    # Make these fields read-only
    readonly_fields = ('docket_id', 'created_at', 'closed_at')

    # You can also define fields to include/exclude for the form
    fields = ('enquiry', 'full_name', 'address', 'phone_number', 'whatsapp_number', 'dob', 
              'problem_facing', 'expected_solution', 'assigned_to', 'status', 'created_by', 'updated_by',)
    
    list_display = (
        'docket_id', 'full_name', 'assigned_to',
        'status', 'created_at', 'updated_by', 'updated_at', 'closed_at',
    )
    list_filter = ('status', 'assigned_to', 'created_at')
    search_fields = ('docket_id', 'full_name', 'phone_number')
    readonly_fields = ('docket_id', 'created_at', 'closed_at')


    inlines = [DocketUpdateLogInline]  # Add inline logs to Docket admin

admin.site.register(Docket, DocketAdmin)



class DocketUpdateLogAdmin(admin.ModelAdmin):
    list_display = ('docket_id', 'updated_by', 'assigned_engineer', 'status', 'updated_at')
    list_filter = ('updated_at', 'updated_by', 'assigned_engineer', 'status')

admin.site.register(DocketUpdateLog, DocketUpdateLogAdmin)