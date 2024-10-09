from django.contrib import admin

# Register your models here.
from .models import Submission

@admin.register(Submission)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname')