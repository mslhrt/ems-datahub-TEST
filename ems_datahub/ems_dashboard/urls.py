from django.urls import path
from .views import list_calls, add_call  # Import views

app_name = 'ems_dashboard'

urlpatterns = [
    path('list/', list_calls, name='list_calls'), 
    path('add/', add_call, name='add_call'),
]
