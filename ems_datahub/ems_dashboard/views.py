from django.shortcuts import render, redirect
from .models import Call
from .forms import CallForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import connection

@login_required
def list_calls(request):
    calls = Call.objects.all().order_by('-date', '-time')  # Order by date and time in descending order
    return render(request, 'ems_dashboard/list_calls.html', {'calls': calls})

@login_required
def add_call(request):
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('ems_dashboard:list_calls'))  # Use reverse to get the URL
    else:
        form = CallForm()
    return render(request, 'ems_dashboard/add_call.html', {'form': form})

class CallUpdateView(LoginRequiredMixin, UpdateView):
    model = Call
    form_class = CallForm
    template_name = 'ems_dashboard/edit_call.html'
    
    def get_success_url(self):
        return reverse_lazy('ems_dashboard:list_calls')

class CallDeleteView(LoginRequiredMixin, DeleteView):
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def query_database(request):
    column_names = []
    query_results = []
    query = ""
    if request.method == "POST":
        if request.user.groups.filter(name='Query Executors').exists():
          query = request.POST.get('query')
          # Ensure only SELECT queries for safety
          if query.lower().strip().startswith("select"):
              with connection.cursor() as cursor:
                  try:
                      cursor.execute(query)
                      column_names = [col[0] for col in cursor.description]
                      query_results = cursor.fetchall()
                  except Exception as e:
                      # Handle the error, maybe return an error message to the user
                      query_results = [[f"Error executing query: {str(e)}"]]
          else:
              query_results = ["Only SELECT queries are allowed."]
        else:
            query_results = ["You do not have permission to execute queries."]
    print(query_results)
    return render(request, 'ems_dashboard/query_database.html', {'column_names': column_names, 'query_results': query_results, 'query': query})

