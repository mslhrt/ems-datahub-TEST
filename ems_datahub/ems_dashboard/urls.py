from django.urls import path
from .views import list_calls, add_call  # Import views

urlpatterns = [
    path('list/', list_calls, name='list_calls'), 
    path('add/', add_call, name='add_call'),
]
