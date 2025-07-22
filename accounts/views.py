from django.shortcuts import render
from django.contrib import auth

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)

        if user:
            print("Login")
        else:
            print("Invalid")

    return render(request, "accounts/login.html")