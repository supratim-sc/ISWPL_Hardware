from django.contrib import admin
from .models import Docket, DocketUpdateLog

# Register your models here.
class DocketAdmin(admin.ModelAdmin):
    # Make these fields read-only
    readonly_fields = ('docket_id', 'created_at', 'closed_at')

    # You can also define fields to include/exclude for the form
    fields = ('enquiry', 'first_name', 'last_name', 'address', 'phone_number', 'whatsapp_number', 'dob', 
              'problem_facing', 'expected_solution', 'assigned_to', 'status', 'created_by',)
    
    list_display = (
        'docket_id', 'first_name', 'last_name', 'assigned_to',
        'status', 'created_at', 'closed_at'
    )
    list_filter = ('status', 'assigned_to', 'created_at')
    search_fields = ('docket_id', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('docket_id', 'created_at', 'closed_at')

admin.site.register(Docket, DocketAdmin)



class DocketUpdateLogAdmin(admin.ModelAdmin):
    list_display = ('docket_id', 'updated_by', 'assigned_engineer', 'status', 'updated_at')
    list_filter = ('updated_at', 'updated_by', 'assigned_engineer', 'status')

admin.site.register(DocketUpdateLog, DocketUpdateLogAdmin)