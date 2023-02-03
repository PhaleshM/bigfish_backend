from email.policy import default
from django.db import models
# Create your models here.
class Faculty(models.Model):
    department= models.CharField(max_length=400)
    designation=models.CharField(
        max_length=20,
        choices=[('Professor','Professor'),('Asst Professor','Asst Professor'),('Associate professor','Associate professor')]
    )
    name = models.CharField(max_length=200)
    dob=models.DateField()
    """l=desig=models.CharField(
        max_length=2,
        choices=[('ug','undergraduate'),('pd','post graduate')])"""
    doa=models.DateField()
    exp=models.IntegerField(default=0)
    regular=models.BooleanField(default=True)
    def __str__(self):
        return self.name

