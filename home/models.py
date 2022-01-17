from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.EmailField(max_length=30)
    content = models.TextField()
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return "message from "+ self.name+ " email - "+ self.email