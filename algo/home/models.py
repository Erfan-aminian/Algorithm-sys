from importlib.util import module_for_loader

from django.db import models
from django.db.models import IntegerField


# Create your models here.
class AlgorithmModel(models.Model):
    OPTION_CHOICES = [
        ('1', 'FCFS'),
        ('2', 'RR'),
        ('3', 'SJF',),
        ('4', 'SRT'),
    ]
    option = models.CharField(max_length=1, choices=OPTION_CHOICES)

class DynamicProcessModel(models.Model):
    process_name = models.PositiveSmallIntegerField()
    arrival_time = models.PositiveSmallIntegerField()
    burst_time = models.PositiveSmallIntegerField()
    quantum = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"process with arrival time:{self.arrival_time} and burst time:{self.burst_time}"


