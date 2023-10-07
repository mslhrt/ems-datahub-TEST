from django.shortcuts import render, redirect
from .models import Call
from .forms import CallForm, DataImportForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import connection
import csv
from io import TextIOWrapper
from django.http import HttpResponse
from django.contrib import messages
from .models import Town, Agency

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
    
    # Fetching table names
    tables = connection.introspection.table_names()

    if request.method == "POST":
        if request.user.groups.filter(name='Query Executors').exists():
          query = request.POST.get('query')
          # Ensure only SELECT queries for safety
          if query.lower().strip().startswith("select"):
              request.session['last_executed_query'] = query
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
    return render(request, 'ems_dashboard/query_database.html', {'column_names': column_names, 'query_results': query_results, 'query': query, 'tables': tables})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def bulk_import(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            csv_file = TextIOWrapper(request.FILES['data_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            
            # Header validation
            expected_headers = ["Date", "Time", "Type of Call", "Responders Count", "Medic Intercept", "Transport Type", "CPR DOS", "Agency Name", "Town Name"]
            if set(reader.fieldnames) != set(expected_headers):
                messages.error(request, "CSV headers do not match the expected format. Please use the template CSV.")
                return redirect('ems_dashboard:bulk_import')
            
            for row in reader:
                # Handle the full-text fields
                try:
                    town = Town.objects.get(name=row['Town Name'])
                    agency = Agency.objects.get(name=row['Agency Name'])
                except (Town.DoesNotExist, Agency.DoesNotExist):
                    messages.error(request, f"Error: Town or Agency not found for row: {row}")
                    continue  # Skip this row and continue with the next
                
                # Map CSV columns to Call model fields
                call_data = {
                    'date': row['Date'],
                    'time': row['Time'],
                    'type_of_call': row['Type of Call'],
                    'responders_count': int(row['Responders Count']),
                    'medic_intercept': row['Medic Intercept'] == 'True',
                    'intercept_agency': agency,
                    'transport_type': row['Transport Type'],
                    'cpr_dos': row['CPR DOS'] == 'True',
                    'town': town
                }

                # Create the Call object
                Call.objects.create(**call_data)
            
            return redirect('ems_dashboard:list_calls')  # or wherever you want to redirect after import
    else:
        form = DataImportForm()
    return render(request, 'ems_dashboard/bulk_import.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_query_result(request):
    # Get the last executed query from the session
    query = request.session.get('last_executed_query', None)
    if not query:
        return HttpResponse("No query result to export.", content_type="text/plain")

    # Execute the query and fetch results
    with connection.cursor() as cursor:
        cursor.execute(query)
        column_names = [col[0] for col in cursor.description]
        query_results = cursor.fetchall()

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="query_result.csv"'
    writer = csv.writer(response)
    writer.writerow(column_names)
    for row in query_results:
        writer.writerow(row)

    return response