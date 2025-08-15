from django.urls import path


from . import views

urlpatterns = [
    path('create_docket/', views.create_docket, name="create_docket"),
    path('view_dockets/', views.view_dockets, name="view_dockets"),
    path('update_docket/<str:docket_id>', views.update_docket, name="update_docket"),
    path('docket_log_add_engineer/<str:docket_id>', views.docket_log_add_engineer, name="docket_log_add_engineer"),
    path('docket_log_update_status/<str:docket_id>/<int:pk>', views.docket_log_update_status, name="docket_log_update_status"),
]