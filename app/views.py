from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import Submission


# def index(request):
def submit_form(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SubmissionForm()

    return render(request, 'index.html', {'form': form})

def index(request):
    l=[]
    malumot=Submission.objects.all()
    print(len(malumot))
    for i in range(len(malumot)):
        l.append(malumot[i])
    return render(request, 'main.html', context={
        'l': l,
        
    })
    