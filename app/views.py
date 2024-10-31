from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import Submission
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,FileResponse,HttpRequest
from django.conf import settings
from config.settings import os
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import re

# def index(request):
def submit_form(request):
    if request.method == 'POST':
        # Get form fields
        fname = request.POST['fname']
        lname = request.POST['lname']
        tel = request.POST['tel']
        city = request.POST['city']
        messagek = request.POST['messagek']
        print(fname, lname, tel, city, messagek)
        
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
        id=Submission.objects.last().id
        # Tayyor PDF fayl yo'li
        template_path = os.path.join(settings.MEDIA_ROOT, 'template.pdf')  # Tayyorlangan PDF faylingiz joylashgan manzil
        output_path = os.path.join(settings.MEDIA_ROOT, f"{fname}_{lname}_{id}_ariza.pdf")  # Saqlash uchun chiqish fayli
        
        print(output_path)
        # Yangi PDF yaratamiz va foydalanuvchi ma'lumotlarini unga qo'shamiz
        packet_path = os.path.join(settings.MEDIA_ROOT, 'packet.pdf')
        packet = canvas.Canvas(packet_path, pagesize=letter)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Shriftni sozlash
        pdfmetrics.registerFont(TTFont('Geologica', os.path.join(settings.MEDIA_ROOT, "Geologica/static/Geologica_Auto-Black.ttf")))
        packet.setFont("Geologica", 12)

        # Foydalanuvchi ma'lumotlarini jadvalga mos joyga qo'shish
        packet.drawString(100, 770, f"id:{id}")
        packet.drawString(100, 750, f"Ismingiz: {fname}")
        packet.drawString(100, 730, f"Familiyangiz: {lname}")
        packet.drawString(100, 710, f"Telefon raqamingiz: {tel}")
        packet.drawString(100, 690, f"Shahar/tuman: {city}")
        packet.drawString(100, 670, f"Huquq buzilish holati:")
        packet.drawString(100, 650, messagek)
        packet.drawString(100, 630, f"Sana: {current_time}")

        # Yangi PDF sahifasini tugatish
        packet.save()

        # Tayyorlangan sahifani tayyor PDF bilan birlashtirish
        template_pdf = PdfReader(template_path)
        overlay_pdf = PdfReader(packet_path)
        output_pdf = PdfWriter()

        # Har bir sahifani birlashtirish
        for page in template_pdf.pages:
        # Asosiy sahifa (template) va qo'shimcha sahifani (overlay) birlashtirish
            merger = PageMerge(page)
            merger.add(overlay_pdf.pages[0]).render()  # Birinchi sahifani qo'shish (packet.pdf faqat bitta sahifadan iborat)
            output_pdf.addpage(page)

    # Chiqish PDF faylini saqlash
    
        with open(output_path, "wb") as f:
            output_pdf.write(f)
        

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
    i=0
    t=[]
    d=[]
    media_files = os.listdir(settings.MEDIA_ROOT)
    for file_name in media_files:
        if re.sub(r'\D', '', file_name[-12:-10])!="":
            t.append(re.sub(r'\D', '', file_name[-12:-10]))
    for file_name in media_files:
        if "ariza" in file_name:
            d.append({"id": int(t[i]), "file": file_name})
            i += 1
            
    print(d)
    print(l[15].id)
    # Submission modelidan barcha ma'lumotlarni olish
     # Ma'lumotlarni list ga aylantirish
    
    # Kontekstni to'g'ri uzatish
    return render(request, 'main.html', context={
        'l': l,
        "d":d,
    
    })

def download_file_ariza(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    print(file_path)
    print(type(settings.MEDIA_ROOT))
    if os.path.exists(file_path):
        response = FileResponse(open(file_path,  'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
    else:
        # Обработка ошибки, если файл не найден
        return HttpResponse("File not found")