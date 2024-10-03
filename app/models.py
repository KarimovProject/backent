from django.db import models

# Create your models here.
from django.db import models

class Submission(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    messagek = models.TextField()

    def __str__(self):
        return f"{self.fname} {self.lname} from {self.city}"
