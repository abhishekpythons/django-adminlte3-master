import csv
import logging

from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import YourModelName
import numpy as np
# from ahp_calculator import ahp_calculator

logger = logging.getLogger(__name__)

variables = {}

def upload_csv(request):

    print("Debug message: This will be printed to the console.")
    if request.method == 'POST':
       
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = form.cleaned_data['csv_file']

                # Process and save the data from the CSV file
                with open(csv_file, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        
                        YourModelName.objects.create(
                            field1=row['field1'],
                            field2=row['field2'],
                            # Add other fields as needed
                             
                        )

                return redirect('success_url')
            except Exception as e:
                logger.error(f"Error processing CSV: {e}")
                # Handle the error or display an error message
        else:
            # Handle form validation errors
            context = {'form': form}
            return render(request, 'upload_csv.html', context)
    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})

# def ahp_calculator(request):
#     # AC=ahp_calculator()
#     if request.method == "POST":
#         criteria = request.POST.get('criteria')
#         value = request.POST.get('value')
#         variables[criteria] = value
#     return render(request, 'adminlte/ahp_calculator.html', {'values':variables})

# # views.py
# from django.shortcuts import render
# import numpy as np

def ahp_calculator(request):
    matrix = None
    priority_vector = None
    criteria_count = request.POST.get('criteria_count')

    if request.method == 'POST' and not criteria_count:
        criteria_count = int(criteria_count)

        if 2 <= criteria_count <= 20:
            matrix = generate_ahp_matrix(request.POST, criteria_count)
            priority_vector = calculate_priority_vector(matrix)

    return render(request, 'adminlte/ahp_calculator.html', {'matrix': matrix, 'priority_vector': priority_vector, 'criteria_count': criteria_count})

def generate_ahp_matrix(post_data, criteria_count):
    matrix = np.ones((criteria_count, criteria_count))

    for i in range(criteria_count):
        for j in range(i + 1, criteria_count):
            comparison_value = int(post_data.get(f'comparison_{i}_{j}'))
            matrix[i, j] = comparison_value
            matrix[j, i] = 1 / comparison_value

    return matrix.tolist()

def calculate_priority_vector(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_eigval_index = np.argmax(eigvals)
    priority_vector = eigvecs[:, max_eigval_index].real
    priority_vector /= np.sum(priority_vector)
    
    return priority_vector.tolist()


def dashboard(request):
    a = 10
    context = {'from_python': a,
    'values':values}
    return render(request, 'adminlte/dashboard.html', context=context)