from django.db import models

class Submission(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    messagek = models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    file=models.FileField(upload_to='files/')

    def __str__(self):
        return f"{self.fname} {self.lname} from {self.city}"
