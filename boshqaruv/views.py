from django.shortcuts import render

def Home(request):

    return render(request, 'admin/index.html')


def Client(request):

    return render(request, 'admin/data-table.html')