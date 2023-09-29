from django.urls import path
from .views import list_calls, add_call, CallUpdateView  # Import views

app_name = 'ems_dashboard'

urlpatterns = [
    path('list/', list_calls, name='list_calls'), #List Calls Page
    path('add/', add_call, name='add_call'), #Add Call Page
    path('edit/<int:pk>/', CallUpdateView.as_view(), name='edit_call'),  # Edit Calls Page
]
