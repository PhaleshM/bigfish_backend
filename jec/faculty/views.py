from re import A
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from .models import Faculty
# Create your views here.
def FacultyData(request):
    fdata=Faculty.objects.all()
    # fname=[a.name for a in fdata]
    # f_name_str="\n".join(fname)
    # return HttpResponse("Our faculty names are:\n>>"+f_name_str)
    Department_query = request.GET.get('Department')
    Teacher_query = request.GET.get('Teacher')
    desig_query=request.GET.get('designation')
    regular_query=request.GET.get('regular')
    print(Department_query)
    if Department_query != '' and Department_query is not None:
        fdata = fdata.filter(department__icontains=Department_query)
    if Teacher_query != '' and Teacher_query is not None:
        fdata = fdata.filter(name__icontains=Teacher_query)
    if (desig_query != 'Choose...' or '') and desig_query is not None:
        fdata = fdata.filter(designation__icontains=desig_query)
    if regular_query != '' and regular_query is not None:
        fdata = fdata.filter(regular=True)
    context={'queryset':fdata}
    return render(request,'faculty/facultydata.html',context)
