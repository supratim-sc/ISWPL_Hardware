from django.urls import path

from . import views

urlpatterns = [
    path('create_enquiry/', views.create_enquiry, name="create_enquiry")
]