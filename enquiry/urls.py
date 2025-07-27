from django.urls import path


from . import views

urlpatterns = [
    path('create_enquiry/', views.create_enquiry, name="create_enquiry"),
    path('view_enquiries/', views.view_enquiries, name="view_enquiries"),
    path('update_enquiry/<str:enquiry_id>', views.update_enquiry, name="update_enquiry"),
]