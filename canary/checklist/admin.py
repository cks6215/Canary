from django.contrib import admin
from .models import EquipmentCategory, Equipment, Reservation, Question
from .models import Checklist

# Register your models here.

admin.site.register(EquipmentCategory)
admin.site.register(Equipment)
admin.site.register(Reservation)
admin.site.register(Question)
admin.site.register(Checklist)