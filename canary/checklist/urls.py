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

    path('makereservation/', views.makereservation, name='makereservation'),

]
