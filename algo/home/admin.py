from django.contrib import admin
from .models import AlgorithmModel, DynamicProcessModel , QuantumModel

# Register your models here.
admin.site.register(AlgorithmModel)
admin.site.register(DynamicProcessModel)
admin.site.register(QuantumModel)