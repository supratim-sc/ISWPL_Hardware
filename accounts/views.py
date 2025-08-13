from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required 

from .models import User

# Create your views here.
def login(request):
    # if post request, then checking details and do accordingly
    if request.method == 'POST':
        # grabbing email and passwod from the submitted form
        email = request.POST['email']
        password = request.POST['password']
        
        # authenticating the user with the provided email and password, if user with those credentials exists
        user = auth.authenticate(email=email, password=password)

        # if user found, then 
        if user:
            # logging in the user and storing the user in the request
            auth.login(request, user)

            # showing the success message
            messages.success(request, f"Welcome back {user.first_name}")

            # redirecting the user to the dashboard page
            return redirect('dashboard')
        
        # if user not found, then
        else:
            # showing the error message
            messages.error(request, 'Invalid credentials! Try again!')

            # redirecting the user to the login page
            return redirect('login')

    # if get request then showing the login form
    return render(request, "accounts/login.html")


# to access the dashboard page user must have to login, 
# if not login then redirect the user to the login page
@login_required(login_url='login')
def dashboard(request):
    # getting the user from the request
    user = request.user
    
    # storing the user object to the context dictionary
    context = {
        'user' : user,
    }

    # rendering the dashboard page with the context dictionary
    return render(request, 'accounts/dashboard.html', context=context)


# for logging out, user must have to be logged in
@login_required(login_url='login')
def logout(request):
    # logging out the user
    auth.logout(request)

    messages.success(request, 'Logged out successfully')

    # after logging out, return the user to the login page
    return redirect('login')


@login_required(login_url='login')
def change_profile_details(request):
    user = request.user

    context = {
        'user' : user,
    }
    return render(request, 'accounts/change_details.html', context)


@login_required(login_url='login')
def update_password(request):
    user = User.objects.get(email__exact = request.user.email)
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        if new_password != confirm_new_password:
            messages.error(request, 'New Password and Confirm New Password does not matches!!')
            return redirect('change_profile_details')
        
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password Updated successfully!!')
        else:
            messages.error(request, 'Incorrect Current Password')

    return redirect('change_profile_details')


@login_required(login_url='login')
def update_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']
        user = request.user
        user.profile_image = profile_image
        user.save()
        messages.success(request, 'Profile image updated successfully!')
    else:
        messages.error(request, 'Please upload a valid image.')

    return redirect('change_profile_details')  # or your preferred redirect