from django.shortcuts import render
from .models import Submission
from django.http import HttpResponse,FileResponse,HttpRequest
from django.conf import settings
from config.settings import os
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import re
import textwrap
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# def index(request):
def submit_form(request):
    if request.method == 'POST':
        # Get form fields
        fname = request.POST['fname']
        lname = request.POST['lname']
        tel = request.POST['tel']
        city = request.POST['city']
        messagek = request.POST['messagek']
        mname = request.POST['mname']
        
        if 'file' in request.FILES:
            file = request.FILES['file']
            # Save the file and other data to the model
            Submission.objects.create(
                fname=fname,
                lname=lname,
                mname=mname,
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
        packet = canvas.Canvas(packet_path, pagesize=A3)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Shriftni sozlash
        pdfmetrics.registerFont(TTFont('Times New Roman', os.path.join(settings.MEDIA_ROOT, "Times New Roman/times new roman.ttf")))
        packet.setFont("Times New Roman", 12)

        # Foydalanuvchi ma'lumotlarini jadvalga mos joyga qo'shish
        
        packet.drawString(250, 495, f"{id}")
        packet.drawString(250, 479, f"{current_time}")
        packet.drawString(250, 463, f"{fname}")
        packet.drawString(250, 447, f"{lname}")
        packet.drawString(250, 431, f"{mname}")
        packet.drawString(250, 431, f"{tel}")
        packet.drawString(250, 415, f"{city}")
        # `messagek` matnini qatorlarga ajratish
        max_line_width = 40  # Har bir qator uchun maksimal belgilar soni (bu sahifa kengligiga bog‘liq holda sozlanishi mumkin)
        wrapped_text = textwrap.wrap(messagek, width=max_line_width)
        start_y = 399  # Boshlang‘ich y-koordinatasi
        line_height = 14  # Qatorlar orasidagi masofa

        for line in wrapped_text:
            packet.drawString(250, start_y, line)
            start_y -= line_height  # Har bir yangi qator uchun y-koordinatani kamaytirish

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
def mark_reviewed(request):
    if request.method == "POST" and request.POST.get("mark_reviewed") == "true":
        ariza_id = request.POST.get("id")
        try:
            ariza = Submission.objects.get(id=ariza_id)
            ariza.reviewed = True
            ariza.save()
            return JsonResponse({"status": "success", "message": "Ariza tekshirilgan deb belgilandi."})
        except Submission.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Ariza topilmadi."})

def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT+"/files", filename)
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
            
    # Kontekstni to'g'ri uzatish
    return render(request, 'main.html', context={
        'l': l,
        "d":d,
    
    })

def download_file_ariza(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path,  'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
    else:
        # Обработка ошибки, если файл не найден
        return HttpResponse("File not found")