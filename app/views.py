from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Submission 


def index(request):
    return render(request, 'index.html')


def submit_form(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        tel = request.POST.get('tel')
        city = request.POST.get('city')
        messagek = request.POST.get('messagek')

        # Save the form data to the database
        Submission.objects.create(
            fname=fname, 
            lname=lname, 
            tel=tel, 
            city=city, 
            messagek=messagek
        )
        return HttpResponse('Your message was sent, thank you!')
    return render(request, 'index.html')
