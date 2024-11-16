"""
URL configuration for health_center project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_patient, name='register_patient'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule_appointment/<int:patient_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('check_in_patient/<int:patient_id>/', views.check_in_patient, name='check_in_patient'),
    path('generate_invoice/<int:patient_id>/', views.generate_invoice, name='generate_invoice'),
]



