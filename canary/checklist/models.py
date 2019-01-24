from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class EquipmentCategory(models.Model):
    category =models.CharField(max_length=20)

    def __unicode__(self):
        return self.category

    def __str__(self):
        return self.category


class Equipment(models.Model):
    item_category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    item_img = models.ImageField()

    def __unicode__(self):
        return self.item_name

    def __str__(self):
        return self.item_name


class Reservation(models.Model):
    email = models.CharField(max_length=20)

    item_category = models.CharField(max_length=20)
    item_name = models.CharField(max_length=20)
    item_id = models.CharField(max_length=10)

    reserved_date = models.DateField(default=datetime.date.today, blank=False)

    start_datetime = models.DateTimeField(unique=False, default=datetime.datetime.now())
    end_datetime = models.DateTimeField(unique=False, default=datetime.datetime.now())

    checklist_complete = models.BooleanField(default=False)
    power = models.CharField(max_length=10, default='off')

    pub_date = models.DateTimeField(max_length=20, default=datetime.datetime.now())

    # result = models.CharField(max_length=20, default='false')

    def __unicode__(self):
        return self.item

    def __str__(self):
        return self.email


class Checklist(models.Model):
    reservation_id = models.CharField(max_length=10)
    author = models.CharField(max_length=20)

    item_name = models.CharField(max_length=20)
    item_id = models.CharField(max_length=10)

    answer = models.TextField()

    pub_date = models.DateTimeField(max_length=20, default=datetime.datetime.now())



class Question(models.Model):
    item_category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text
