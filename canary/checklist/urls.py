"""canary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'checklist'

urlpatterns = [
    path('main/<category>', views.main, name='main'),

    path('reservation_page/<item_id>/', views.reservation_page, name='reservation_page'),
    path('reservation_page/<item_id>/<item_date>/', views.datepicker, name='datepicker'),
    path('reserved/', views.reserved, name='reserved'),

    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('delete_reservation/<reservation_id>', views.delete_reservation, name='delete_reservation'),

    path('checklist_page/<reservation_id>/', views.checklist_page, name='checklist_page'),
    path('make_checklist/<reservation_id>/', views.make_checklist, name='make_checklist'),
    path('control_page/<reservation_id>/<power>/', views.control_page, name='control_page'),
    path('control_power/<item_id>/', views.control_power, name='control_power'),
]
