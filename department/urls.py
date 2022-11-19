"""College_Election URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('AddStudent/',views.addstud,name='addstud'),
    path('AddStudent/validate_addstud/',views.validate_addstud,name='Validate_addstud'),
    path('DeptEdit/',views.deptedit,name='deptedit'),
    path('DeptEdit/validate_dept_edit/',views.validate_dept_edit,name='validate_dept_edit'),

]
