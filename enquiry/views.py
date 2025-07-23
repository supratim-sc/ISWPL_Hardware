from django.shortcuts import render, redirect
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