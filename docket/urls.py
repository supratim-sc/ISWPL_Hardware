from django.urls import path


from . import views

urlpatterns = [
    path('create_docket/', views.create_docket, name="create_docket"),
    path('view_dockets/', views.view_dockets, name="view_dockets"),
    # path('update_enquiry/<str:enquiry_id>', views.update_enquiry, name="update_enquiry"),
]