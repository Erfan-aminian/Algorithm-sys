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

class CountModel(models.Model):
    count = models.PositiveIntegerField(
        verbose_name='Number of processes',
        help_text='Number of processes (between 1 and 9)'
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"count:{self.count}"

class FcfsProcessModel(models.Model):
    fcfs_algorithm = models.ForeignKey(CountModel, related_name='fcfs_algorithms', on_delete=models.CASCADE)
    execution_time = models.PositiveIntegerField(verbose_name='execution time')

