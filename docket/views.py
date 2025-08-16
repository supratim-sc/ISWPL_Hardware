from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from accounts.models import User

from .models import Docket, DocketUpdateLog, STATUS_CHOICES
from .forms import DocketForm, DocketUpdateLogForm


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
    dockets = Docket.objects.all().order_by('-created_at')

    return render(request, 'docket/view_dockets.html', context={'dockets' : dockets})


@login_required(login_url='login')
@role_required("ADMIN", "ADVISER")
def update_docket(request, docket_id):
    docket = get_object_or_404(Docket, docket_id=docket_id)
    docket_logs = DocketUpdateLog.objects.filter(docket_id=docket).order_by('-pk')

    # POST: creating a new log and/or updating docket info
    if request.method == 'POST':
        docket_form = DocketForm(request.POST, instance=docket)

        if docket_form.is_valid():
            docket_instance = docket_form.save(commit=False)
            docket_instance.updated_by = request.user
            docket_instance.save()
            messages.success(request, 'Docket updated successfully')
            return redirect('update_docket', docket_id=docket.docket_id)
    
    else:
        docket_form = DocketForm(instance=docket)
        docket_update_log_form = DocketUpdateLogForm()

    # Build a list of (log, form) pairs
    docket_log_forms = [
        (log, DocketUpdateLogForm(instance=log)) for log in docket_logs
    ]

    return render(request, 'docket/update_docket.html', {
        'docket': docket,
        'docket_form': docket_form,
        'docket_update_log': docket_logs,
        'docket_update_log_form': docket_update_log_form,  # for new logs
        'docket_log_forms': docket_log_forms,              # for existing logs
    })



@login_required(login_url='login')
@role_required("ADMIN", "ADVISER")
def docket_log_add_engineer(request, docket_id):
    docket = get_object_or_404(Docket, docket_id=docket_id)


    if request.method == 'POST':
        assigned_engineer_id = request.POST['assigned_engineer']
        last_log = DocketUpdateLog.objects.filter(docket_id=docket).last()
        previous_status = last_log.status if last_log else STATUS_CHOICES[0][0]
        
        DocketUpdateLog.objects.create(
            docket_id=docket,
            assigned_engineer=User.objects.get(pk=assigned_engineer_id),
            updated_by=request.user,
            status=previous_status,
        )
        messages.success(request, "Engineer assigned to docket successfully")
        return redirect('update_docket', docket_id=docket.docket_id)

    # If GET or invalid
    return redirect('update_docket', docket_id=docket.docket_id)


@login_required(login_url='login')
@role_required("ADMIN", "ADVISER")
def docket_log_update_status(request, docket_id, pk):
    docket = get_object_or_404(Docket, docket_id=docket_id)
    docket_update_log = get_object_or_404(DocketUpdateLog, pk=pk, docket_id=docket)

    print(docket_update_log, docket_id, pk)
    # Capture current engineer before form binding
    original_engineer = docket_update_log.assigned_engineer

    if request.method == 'POST':
        # Do NOT try to set initial here — it won't work with POST
        docket_update_log_form = DocketUpdateLogForm(request.POST, instance=docket_update_log)

        if docket_update_log_form.is_valid():
            log_entry = docket_update_log_form.save(commit=False)

            # Explicitly restore original assigned_engineer if it's None
            log_entry.assigned_engineer = original_engineer
            log_entry.updated_by = request.user
            log_entry.save()

            messages.success(request, "Docket Log updated successfully")
            return redirect('update_docket', docket_id=docket.docket_id)

    return redirect('update_docket', docket_id=docket.docket_id)

