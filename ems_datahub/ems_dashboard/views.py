from django.shortcuts import render, redirect
from .models import Call
from .forms import CallForm

def list_calls(request):
    calls = Call.objects.all()
    return render(request, 'ems_dashboard/list_calls.html', {'calls': calls})

def add_call(request):
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_calls')
    else:
        form = CallForm()
    return render(request, 'ems_dashboard/add_call.html', {'form': form})