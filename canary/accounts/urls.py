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

app_name = 'accounts'

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('register_page/', views.register_page, name='register_page'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('checklist_page/<reservation_id>/', views.checklist_page, name='checklist_page'),
    path('makechecklist/<reservation_id>/', views.makechecklist, name='makechecklist'),
    path('control_page/<reservation_id>/<power>/', views.control_page, name='control_page'),
    # path('control/<item_id>/', views.control, name='control'),
]