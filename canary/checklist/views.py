import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Reservation, Equipment, EquipmentCategory


# Create your views here.

def main(request, category):
    if category == 'All':
        equipments_li = Equipment.objects.all()

    else:
        tmp_category = EquipmentCategory.objects.get(category=category)
        equipments_li = Equipment.objects.filter(item_category=tmp_category)

    context = {
        'category':category,
        'equipments':equipments_li
    }
    return render(request, 'checklist/main.html', context)


def reservation_page(request, item_id):
    form = ReservationForm()
    equipment = get_object_or_404(Equipment, pk=item_id)

    context = {
        'form': form,
        'equipment':equipment
    }
    return render(request, 'checklist/reservation_page.html', context)


def datepicker(request, item_id, item_date):
    available_dict = {
        '0': 'available', '1': 'available', '2': 'available', '3': 'available',
        '4': 'available', '5': 'available', '6': 'available', '7': 'available',
        '8': 'available', '9': 'available', '10': 'available', '11': 'available',
        '12': 'available', '13': 'available', '14': 'available', '15': 'available',
        '16': 'available', '17': 'available', '18': 'available', '19': 'available',
        '20': 'available', '21': 'available', '22': 'available', '23': 'available',
    }

    tmp_item_date = datetime.datetime.strptime(item_date, '%Y-%m-%d')
    reservation_li = Reservation.objects.filter(item_id=item_id, reserved_date=tmp_item_date)

    if tmp_item_date.date() == datetime.datetime.now().date():
        for i in range(0,24):
            if i < datetime.datetime.now().hour:
                available_dict[i] = 'unavailable'

    for re in reservation_li:
        tmp_start_datetime = re.start_datetime.replace(tzinfo=None)+datetime.timedelta(hours=9)
        tmp_end_datetime = re.end_datetime.replace(tzinfo=None)+datetime.timedelta(hours=9)

        for i in range(0, 24):
            datetime_object = tmp_item_date+datetime.timedelta(hours=i)

            if datetime_object == tmp_start_datetime:
                start_h = tmp_start_datetime.hour
                end_h = tmp_end_datetime.hour

                for i in range(start_h, end_h+1):
                    available_dict[i] = 'unavailable'

    response = {'status': 'success', 'message':'', 'time':available_dict}
    return HttpResponse(json.dumps(response), content_type='application/json')



def reserved(request):
    return render(request, 'checklist/main.html', {})


def makereservation(request):
    if request.method == 'POST':
        tmp_email = request.user.username
        tmp_item_id = request.POST.get('item_id')
        tmp_item_category = request.POST.get('item_category')
        tmp_item_name = request.POST.get('item_name')
        tmp_reserved_date = datetime.datetime.strptime(request.POST.get('item_date'), '%Y-%m-%d')
        tmp_start_time = datetime.datetime.strptime(request.POST.get('start_time'), '%H:%M')
        tmp_end_time = datetime.datetime.strptime(request.POST.get('end_time'), '%H:%M')
        tmp_start_datetime = tmp_reserved_date + datetime.timedelta(hours=tmp_start_time.hour, minutes=tmp_start_time.minute)
        tmp_end_datetime = tmp_reserved_date + datetime.timedelta(hours=tmp_end_time.hour, minutes=tmp_end_time.minute)

        Reservation.objects.create(email=tmp_email,
                                   item_id=tmp_item_id,
                                   item_category=tmp_item_category,
                                   item_name=tmp_item_name,
                                   reserved_date=tmp_reserved_date,
                                   start_datetime=tmp_start_datetime,
                                   end_datetime=tmp_end_datetime,
                                   pub_date=datetime.datetime.now(),
                                   )
        response = {'status':'success', 'message':'예약되었습니다.'}
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        return redirect('checklist:main')


# def checklist_complete(request, item_id):
#     reservation_li = Reservation.objects.filter(item_id=item_id)
#     tmp_reservation = Reservation()
#
#     for re in reservation_li:
#         if re.start_datetime < datetime.datetime.now() and datetime.datetime.now() < re.end_datetime:
#             tmp_reservation = re
#             break
#
#     if tmp_reservation.checklist_complete == True:
#         return HttpResponse