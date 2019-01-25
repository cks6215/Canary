import datetime
from django.utils import timezone
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Reservation, Equipment, EquipmentCategory, Question, Checklist


# Create your views here.

def main(request, category):
    try:
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

    except:
        context = {
            'category': category,
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


def make_reservation(request):

    reservation_li = []

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

        for r in Reservation.objects.filter(email=tmp_email, end_datetime__gte=timezone.now()):
            reservation_li.append(r)

        if len(reservation_li)<3:
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
            response = {'status':'fail', 'message':'동시에 3개까지만 예약할 수 있습니다.'}
            return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        return redirect('checklist:main')


def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.delete()

    return redirect('accounts:mypage')

def checklist_page(request, reservation_id):

    reservation = get_object_or_404(Reservation, pk=reservation_id)
    equipment = get_object_or_404(Equipment, pk=reservation.item_id)
    question_li = Question.objects.filter(item_category = equipment.item_category)

    if reservation.checklist_complete == True:
        return redirect('checklist:control_page', reservation.id, 'off')

    if reservation.email.find('@') != -1:

        index = reservation.email.find('@')
        username = reservation.email[0:index]

    else:
        username = reservation.email

    context = {'question_li':question_li,
               'reservation':reservation,
               'username':username}

    return render(request, 'checklist/checklist_page.html', context)


def make_checklist(request, reservation_id):

    if request.method == 'POST':

        reservation = get_object_or_404(Reservation, pk=reservation_id)
        equipment = get_object_or_404(Equipment, pk=reservation.item_id)
        question_li = Question.objects.filter(item_category=equipment.item_category)

        tmp_reservation_id = reservation_id
        tmp_author = reservation.email
        tmp_item_name = reservation.item_name
        tmp_item_id = reservation.item_id
        tmp_answer_li = {}

        for q in question_li:
            tmp_answer_li[q.text] = request.POST.get('response'+str(q.id))

        Checklist.objects.create(
            reservation_id=tmp_reservation_id,
            author=tmp_author,
            item_name=tmp_item_name,
            item_id=tmp_item_id,
            answer=str(tmp_answer_li),
            pub_date= datetime.datetime.now(),
        )

        # 에약 객체에 체크리스트 제출 여부 속성 추가.

        reservation.checklist_complete = True
        reservation.save()

        response = {'status':'success', 'message':'제출되었습니다.'}
        return HttpResponse(json.dumps(response), content_type='application/json')

    else: #체크리스트 점검하는 알고리즘 추가
        response = {'status': 'fail', 'message': '다시 작성하세요'}
        return HttpResponse(json.dumps(response), content_type='application/json')


def control_page(request, reservation_id, power):
    if request.user.is_authenticated:
        reservation = Reservation.objects.get(pk=reservation_id)

        if request.user.username == reservation.email:
            reservation.power = power
            reservation.save()

            context = {
                'reservation':reservation
            }

            return render(request, 'checklist/control_page.html', context)

        else:
            return redirect('accounts:login_page')

    else:
        return redirect('accounts:login_page')


def control_power(request, item_id):

    reservation_li = Reservation.objects.filter(item_id=item_id)
    reservation = Reservation()

    for re in reservation_li:
        tmp_start_datetime = re.start_datetime.replace(tzinfo=None) + datetime.timedelta(hours=9)
        tmp_end_datetime = re.end_datetime.replace(tzinfo=None) + datetime.timedelta(hours=9)

        if tmp_start_datetime < datetime.datetime.now() and datetime.datetime.now() < tmp_end_datetime:
            reservation = re
        break

    if reservation.power == 'on':
        response = 'on'
        return HttpResponse(response)

    else:
        response = 'off'
        return HttpResponse(response)