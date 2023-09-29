from django.shortcuts import render, redirect
from .models import Call
from .forms import CallForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

def list_calls(request):
    calls = Call.objects.all().order_by('-date', '-time')  # Order by date and time in descending order
    return render(request, 'ems_dashboard/list_calls.html', {'calls': calls})

def add_call(request):
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('ems_dashboard:list_calls'))  # Use reverse to get the URL
    else:
        form = CallForm()
    return render(request, 'ems_dashboard/add_call.html', {'form': form})

class CallUpdateView(UpdateView):
    model = Call
    form_class = CallForm
    template_name = 'ems_dashboard/edit_call.html'
    
    def get_success_url(self):
        return reverse_lazy('ems_dashboard:list_calls')

class CallDeleteView(DeleteView):
    model = Call
    template_name = 'ems_dashboard/delete_call.html'
    
    def get_success_url(self):
        return reverse_lazy('ems_dashboard:list_calls')