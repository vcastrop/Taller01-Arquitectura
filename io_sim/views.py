from django.shortcuts import render

def index(request):
    return render(request, 'io_sim/io_sim.html')