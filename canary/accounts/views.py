
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


