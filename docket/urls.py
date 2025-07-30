from django.urls import path


from . import views

urlpatterns = [
    path('create_docket/', views.create_docket, name="create_docket"),
    # path('view_enquiries/', views.view_enquiries, name="view_enquiries"),
    # path('update_enquiry/<str:enquiry_id>', views.update_enquiry, name="update_enquiry"),
]