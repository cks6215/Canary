
import json
import datetime
from django.utils import timezone

from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import (login as login_auth, logout as logout_auth, authenticate)
from django.contrib.auth.models import User

from checklist.models import Reservation, Equipment, Question, Checklist
from .forms import RegistrationForm, AuthenticationForm


def login_page(request):
    form = AuthenticationForm()

    return render(request, 'accounts/login_page.html', {'form':form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)

        if form.is_valid():
            tmp_username = request.POST.get('username')
            tmp_password = request.POST.get('password')

            user = authenticate(username=tmp_username, password=tmp_password)

            if user is not None:
                login_auth(request, user)
                response = {'status':'success', 'message':'로그인'}

                return HttpResponse(json.dumps(response), content_type='application/json')

            elif User.objects.filter(username=tmp_username).exists():
                response = {'status': 'fail', 'message': "Email and password do not match. please check again."}
                return HttpResponse(json.dumps(response), content_type='application/json')

            else:
                response = {'status':'fail', 'message': "Not Register."}
                return HttpResponse(json.dumps(response), content_type='application/json')


    else:
        return render(request, 'accounts/login_page.html', {})


def register_page(request):
    form = RegistrationForm()

    return render(request, 'accounts/register_page.html', {'form':form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            tmp_username = request.POST.get('username')
            tmp_password1 = request.POST.get('password1')
            tmp_password2 = request.POST.get('password2')

            if tmp_password1 != tmp_password2:
                response = {'status':'fail', 'message': "password1 and password2 verification do not match. Please check again."}
                return HttpResponse(json.dumps(response), content_type='application/json')
            elif tmp_username.find('.') == -1 or tmp_username.find('@') == -1:
                response = {'status':'fail', 'message': "Inappropriate email address. Please enter a valid email address."}
                return HttpResponse(json.dumps(response), content_type='application/json')
            elif tmp_username.find("unist.ac.kr") == -1:
                response = {'status':'fail', 'message': "This is not UNIST email address. Please enter a valid email address"}
                return HttpResponse(json.dumps(response), content_type='application/json')
            elif User.objects.filter(username=tmp_username).exists():
                response = {'status':'fail', 'message': "This username already exists. Please enter another username."}
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                user = User.objects.create_user(
                    username=tmp_username,
                    password=tmp_password1,
                )

                response = {'status': 'success', 'message': "Welcome!!"}
                return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return redirect('login_page')
    return render(request, 'accounts/login_page.html', {})


def logout(request):
    logout_auth(request)

    return redirect('accounts:login_page')


def mypage(request):
    reservations = Reservation.objects.filter(email=request.user.username, end_datetime__gte=timezone.now())
    reservation_li = []



    for re in reservations:
        tmp_start_datetime = re.start_datetime.replace(tzinfo=None) + datetime.timedelta(hours=9)
        tmp_end_datetime = re.end_datetime.replace(tzinfo=None) + datetime.timedelta(hours=9)

        item = Equipment.objects.get(pk=re.item_id)
        start_datetime = datetime.datetime.strftime(tmp_start_datetime, '%Y-%m-%d %H:%M')
        end_datetime = datetime.datetime.strftime(tmp_end_datetime, '%Y-%m-%d %H:%M')

        reservation_li.append((re, item, start_datetime, end_datetime))

    context = {'reservation_li': reservation_li}
    return render(request, 'accounts/mypage.html', context)


def checklist_page(request, reservation_id):

    reservation = get_object_or_404(Reservation, pk=reservation_id)
    equipment = get_object_or_404(Equipment, pk=reservation.item_id)
    question_li = Question.objects.filter(item_category = equipment.item_category)

    if reservation.checklist_complete == True:
        return redirect('accounts:control_page', reservation.id, 'off')

    if reservation.email.find('@') != -1:

        index = reservation.email.find('@')
        username = reservation.email[0:index]

    else:
        username = reservation.email

    context = {'question_li':question_li,
               'reservation':reservation,
               'username':username}

    return render(request, 'accounts/checklist_page.html', context)


def makechecklist(request, reservation_id):

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
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.power = power

    reservation.save()

    context = {
        'reservation':reservation
    }

    return render(request, 'accounts/control_page.html', context)


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