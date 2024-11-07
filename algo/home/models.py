from django.db import models

# Create your models here.
class AlgorithmModel(models.Model):
    OPTION_CHOICES = [
        ('1', 'FCFS'),
        ('2', 'RR'),
        ('3', 'SJF',),
        ('4', 'SRT'),
    ]
    option = models.CharField(max_length=1, choices=OPTION_CHOICES)
