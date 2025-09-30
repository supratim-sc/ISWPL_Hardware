from django import forms

from .models import Docket, DocketUpdateLog

from accounts.models import User

class DocketForm(forms.ModelForm):
    class Meta:
        model = Docket
        exclude = ['docket_id', 'status', 'created_at', 'updated_at', 'created_by', 'updated_by', 'updated_log', 'closed_at',]  # exclude auto-generated fields
        widgets = {
            'enquiry': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'problem_facing': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'expected_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # Dropdowns (ForeignKey)
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),

        }

    # FOR ONLY SHOWING ACTIVE ADVISERs
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['assigned_to'].queryset = User.objects.filter(role="ADVISER", is_active=True)
        self.fields['assigned_to'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


class DocketUpdateLogForm(forms.ModelForm):
    class Meta:
        model = DocketUpdateLog
        exclude = {'docket_id', 'updated_by', 'updated_at'}
        widgets = {
            'assigned_engineer' : forms.Select(attrs = {'class' : 'form-select'}),
            'status' : forms.Select(attrs = {'class' : 'form-select'}),
        }
