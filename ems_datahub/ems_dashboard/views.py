from django.shortcuts import render
from .models import Call

def list_calls(request):
    calls = Call.objects.all()
    return render(request, 'ems_dashboard/list_calls.html', {'calls': calls})