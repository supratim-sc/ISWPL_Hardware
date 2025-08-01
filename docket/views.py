from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import Docket, DocketUpdateLog
from .forms import DocketForm

from enquiry.models import Enquiry
# Create your views here.

def role_required(*roles):
    def check(user):
        if user.role in roles:
            return True
        raise PermissionDenied
    return user_passes_test(check)



@login_required(login_url='login')
@role_required('ADMIN', 'RECEPTIONIST')
def create_docket(request):
    enquiry = None
    docket_form = DocketForm()

    if request.method == 'GET':
        enquiry_id = request.GET.get('enquiry_id', '').strip()

        # Fetch button clicked
        if enquiry_id :
            try:
                enquiry = Enquiry.objects.get(enquiry_id=enquiry_id)
                messages.success(request, 'Enquiry details found and filled!!')

                # Pre-fill form fields from Enquiry
                docket_form = DocketForm(
                    initial={
                        'enquiry': enquiry.id,
                        'first_name': enquiry.first_name,
                        'last_name': enquiry.last_name,
                        'phone_number': enquiry.phone_number,
                        'whatsapp_number': enquiry.whatsapp_number,
                        'address': enquiry.address,
                    }
                )

            except Enquiry.DoesNotExist:
                messages.error(request, 'No enquiry found with the specified Enquiry ID.')
                docket_form = DocketForm()
    
    if request.method == 'POST':
        # Form submission
        docket_form = DocketForm(request.POST)
        if docket_form.is_valid():
            docket = docket_form.save(commit=False)
            docket.created_by = request.user  # auto-track creator
            docket.save()
            messages.success(request, f'Docket {docket.docket_id} created successfully.')
            return redirect('create_docket')  # or redirect to the docket detail page

    return render(request, 'docket/create_docket.html', {
        'docket_form': docket_form,
        'enquiry': enquiry,
    })



@login_required(login_url='login')
@user_passes_test(role_required("ADMIN", "RECEPTIONIST", "ADVISER"))
def view_dockets(request):
    dockets = Docket.objects.prefetch_related('docket_update_log').all().order_by('-created_at')

    return render(request, 'docket/view_dockets.html', context={'dockets' : dockets})