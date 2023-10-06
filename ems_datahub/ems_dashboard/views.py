from django.shortcuts import render, redirect
from .models import Call
from .forms import CallForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
import json
from django.contrib.auth.decorators import user_passes_test
from django.db import connection


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

def dashboard(request):
    data = {
        'labels': ['January', 'February', 'March', 'April'],
        'datasets': [{
            'label': 'Number of Calls',
            'data': [65, 59, 80, 81],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }

    options = {
        'scales': {
            'y': {
                'beginAtZero': True
            }
        }
    }

    context = {
        'data': json.dumps(data),
        'options': json.dumps(options)
    }
    return render(request, 'ems_dashboard/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def query_database(request):
    results = []
    query = ""
    if request.method == "POST":
        query = request.POST.get('query')
        # Ensure only SELECT queries for safety
        if query.lower().strip().startswith("select"):
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    results = cursor.fetchall()
                except Exception as e:
                    # Handle the error, maybe return an error message to the user
                    results = [f"Error executing query: {str(e)}"]
        else:
            results = ["Only SELECT queries are allowed."]
    return render(request, 'ems_dashboard/query_database.html', {'results': results, 'query': query})
