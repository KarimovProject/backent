from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import Submission
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,FileResponse,HttpRequest
from django.conf import settings
from config.settings import os


# def index(request):
def submit_form(request):
    if request.method == 'POST':
        # Get form fields
        fname = request.POST['fname']
        lname = request.POST['lname']
        tel = request.POST['tel']
        city = request.POST['city']
        messagek = request.POST['messagek']
        
        # Handle file upload
        if 'file' in request.FILES:
            file = request.FILES['file']
            # Save the file and other data to the model
            Submission.objects.create(
                fname=fname,
                lname=lname,
                tel=tel,
                city=city,
                messagek=messagek,
                file=file  # Directly assign the uploaded file to the model
            )

    return render(request, 'index.html')

def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT+"/files", filename)
    print(file_path)
    print(type(settings.MEDIA_ROOT))
    if os.path.exists(file_path):
        response = FileResponse(open(file_path,  'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
    else:
        # Обработка ошибки, если файл не найден
        return HttpResponse("File not found")


def index(request):
    # PDF fayl yo'li
    malumot = Submission.objects.all()
    l = list(malumot) 
    
    
    # Submission modelidan barcha ma'lumotlarni olish
     # Ma'lumotlarni list ga aylantirish
    
    # Kontekstni to'g'ri uzatish
    return render(request, 'main.html', context={
        'l': l
    })

    