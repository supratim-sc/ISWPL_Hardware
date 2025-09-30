from django import forms
from .models import Enquiry, TeleCaller

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        exclude = ['enquiry_id', 'created_at', 'updated_at', 'created_by', 'updated_by']  # exclude auto-generated fields
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'service_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'customer_reference_name': forms.TextInput(attrs={'class': 'form-control'}),

            # Dropdowns (ForeignKey)
            'enquiry_type': forms.Select(attrs={'class': 'form-select'}),
            'reference_type': forms.Select(attrs={'class': 'form-select'}),
            'tele_caller_name': forms.Select(attrs={'class': 'form-select'}),
        }

    # FOR ONLY SHOWING ACTIVE TELE CALLERS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tele_caller_name'].queryset = TeleCaller.objects.filter(is_active=True)