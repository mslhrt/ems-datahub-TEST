from django.shortcuts import render
from .models import CallData  # Import other models as needed

def dashboard(request):
    call_data = CallData.objects.all()  # Retrieve all call data from the database
    context = {'call_data': call_data}
    return render(request, 'ems_dashboard/dashboard.html', context)
