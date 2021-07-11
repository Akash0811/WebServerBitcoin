from django.db import models

# Create your models here.
class Alert(models.Model):
    d1 = models.CharField(max_length=8)
    t1 = models.CharField(max_length=5)
    price = models.FloatField( default = 0.0 )
