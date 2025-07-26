from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required 

from .forms import EnquiryForm
from .models import Enquiry, EnquiryType, TeleCaller, ReferenceType

@login_required(login_url='login')
def create_enquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)  # enquiry_id is auto-created in model's save()
            enquiry.created_by = request.user  # Set created_by to current user
            enquiry.updated_by = request.user  # Set updated_by to current user
            enquiry.save()  # Now save to DB
            messages.success(request, f'Enquiry generate with enquiry id: {enquiry.enquiry_id}')
            return redirect('create_enquiry')

    form = EnquiryForm()

    return render(request, 'enquiry/create_enquiry.html', {'form': form,})


@login_required(login_url='login')
def view_enquiries(request):
    enquiries = Enquiry.objects.all().order_by('-created_at')
    
    return render(request, 'enquiry/view_enquiries.html', context={'enquiries' : enquiries})


@login_required(login_url='login')
def update_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, enquiry_id=enquiry_id)

    if request.method == 'POST':
        enquiry_form = EnquiryForm(request.POST, instance=enquiry)
        if enquiry_form.is_valid():
            enquiry_form.save()
            messages.success(request, f'Enquiry details for {enquiry.enquiry_id} updated successfully!')
            return redirect('view_enquiries')  # redirect to detail or success page
    else:
        enquiry_form = EnquiryForm(instance=enquiry)

    return render(request, 'enquiry/update_enquiry.html', {
        'enquiry_form': enquiry_form,
        'enquiry': enquiry,
    })

    # if request.method == 'POST':
    #     form = EnquiryForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Enquiry updated successfully!!')
    #         return redirect('view_enquiries')
    # try:
    #     enquiry = Enquiry.objects.get(enquiry_id=enquiry_id)
    # except Enquiry.DoesNotExist:
    #     return render(request, 'enquiry/enquiry_not_found.html', context={'enquiry_id' : enquiry_id})


    # enquiry_form = EnquiryForm(instance=enquiry)
    # return render(request, 'enquiry/update_enquiry.html', context={'enquiry_form': enquiry_form, 'enquiry' : enquiry})