from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('change_profile_details/', views.change_profile_details, name='change_profile_details'),
    path('change_password/', views.change_password, name='change_password'),
]