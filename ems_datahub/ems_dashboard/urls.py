from django.urls import path
from .views import list_calls, add_call, CallUpdateView, CallDeleteView, dashboard    # Import views

app_name = 'ems_dashboard'

urlpatterns = [
    path('list/', list_calls, name='list_calls'), #list_calls View
    path('add/', add_call, name='add_call'), #add_call View
    path('edit/<int:pk>/', CallUpdateView.as_view(), name='edit_call'),  # Update View
    path('delete/<int:pk>/', CallDeleteView.as_view(), name='delete_call'),  # Delete View
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard View
]
