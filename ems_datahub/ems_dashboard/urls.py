from django.urls import path
from .views import list_calls  # Import the new view

urlpatterns = [
    path('list/', list_calls, name='list_calls'),  # Add a new path for the list view
]
