from django import forms
from .models import Reservation
import datetime

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        widgets = {'reserved_date': forms.DateInput(attrs={'class':'datepicker'})}
        exclude = ['email', 'item_category' ,'item_name', 'pub_date', 'start_datetime', 'end_datetime']
