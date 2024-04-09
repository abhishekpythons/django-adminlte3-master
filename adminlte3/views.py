import csv
import logging

from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import YourModelName
import numpy as np
# from ahp_calculator import ahp_calculator

from django.template.defaulttags import register

RI_table = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51]

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')


@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_range_matrix(matrix):
    return range(len(matrix))

@register.filter
def get_range_from_1(value):
    return range(value+1)[1:value+1]


@register.filter
def get_element_by_index(lst, index):
    return lst[index]

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

def criteria_count(request):
    criteria_count = None
    if request.method == 'POST':
        criteria_count = int(request.POST.get('criteria_count'))
        c1 = request.POST.get('criteria_1')
        if c1:
            criteria_names=[]
            criteria_names.append(c1)
            for i in range(2,criteria_count+1):
                criteria_names.append(request.POST.get(f'criteria_{i}'))
            return render(request, 'ahp_priority_values.html', {'criteria_count': criteria_count, 'criteria_names':criteria_names})
    return render(request, 'ahp_criteria_count.html', {'criteria_count':criteria_count})

def generate_ahp_matrix(post_data, criteria_count):
    matrix = np.ones((criteria_count, criteria_count))

    for i in range(criteria_count):
        for j in range(i + 1, criteria_count):
            comparison_value = int(post_data.get(f'comparison_{i}_{j}'))
            isAwrtB = True if post_data.get(f'isAwrtB_{i}_{j}') == 'True' else False
            if isAwrtB:
                matrix[i, j] = comparison_value
                matrix[j, i] = 1 / comparison_value
            else:
                matrix[i, j] = 1 / comparison_value
                matrix[j, i] = comparison_value


    return matrix

def calculate_priority_vector(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_eigval_index = np.argmax(eigvals)
    priority_vector = eigvecs[:, max_eigval_index].real
    priority_vector /= np.sum(priority_vector)
    
    return priority_vector, eigvals[max_eigval_index]

def round_values(data, decimal_places):
    if isinstance(data, list):
        return [round(value, decimal_places) for value in data]
    elif isinstance(data, np.ndarray):
        return np.round(data, decimal_places)
    else:
        return round(data, decimal_places)

def calculate_ahp(request):
    matrix = None
    priority_vector = None

    if request.method == 'POST':
        criteria_count = int(request.POST.get('criteria_count'))
        criteria_names = request.POST.get('criteria_names')
        criteria_names = ' '+criteria_names[1:-1]
        criteria_names = [ele[2:-1] for ele in criteria_names.split(',')]
        matrix = generate_ahp_matrix(request.POST, criteria_count)
        priority_vector, max_eigen = calculate_priority_vector(matrix)
        ranks = [criteria_count-list(np.argsort(priority_vector)).index(i) for i in range(criteria_count)]
        priority_vector_percentage = 100*priority_vector
        max_eigen=round(max_eigen, 3)   
        ci=(max_eigen-criteria_count)/(criteria_count-1)
        ri=RI_table[criteria_count-1]
        cr=ci/ri
        cr=round(cr, 3)
        return render(request, 'ahp_results.html', {'matrix': round_values(matrix, 2), 'priority_vector': round_values(priority_vector_percentage, 2), 'criteria_count': criteria_count, 'criteria_names':criteria_names, 'ranks':ranks, 'cr':cr.real, 'max_eigen':max_eigen.real})
    return(redirect('home'))


def dashboard(request):
    a = 10
    context = {'from_python': a,
    'values':values}
    return render(request, 'adminlte/dashboard.html', context=context)