from django.urls import path
from .views import list_calls, add_call, CallUpdateView, CallDeleteView, dashboard, query_database, bulk_import, export_query_result  # Import views

app_name = 'ems_dashboard'

urlpatterns = [
    path('list/', list_calls, name='list_calls'),  # list_calls View
    path('add/', add_call, name='add_call'),  # add_call View
    path('edit/<int:pk>/', CallUpdateView.as_view(), name='edit_call'),  # Update View
    path('delete/<int:pk>/', CallDeleteView.as_view(), name='delete_call'),  # Delete View
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard View
    path('query_database/', query_database, name='query_database'),  # Database Query View
    path('bulk_import/', bulk_import, name='bulk_import'),
    path('export_query_result/', export_query_result, name='export_query_result'),
]
