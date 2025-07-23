from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required 

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

            # redirecting the user to the dashboard page
            return redirect('dashboard')
        
        # if user not found, then
        else:
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

    # after logging out, return the user to the login page
    return redirect('login')