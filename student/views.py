from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse
from tables.models import *
import datetime
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
import math, random
from django.core import serializers


def getName(request):
    t_did = request.session['id']
    t_d = student.objects.get(stud_id=t_did)
    t_name = t_d.stud_fname + ' ' + t_d.stud_mname + ' ' + t_d.stud_lname
    return t_name

# Create your views here.
def home(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    """ check for valid stud """
    t_name = getName(request)

    sid = request.session['id']

    e = election.objects.filter(elect_status=0)

    if e.count() > 0:

        e = election.objects.get(elect_status=0)
        ep = election_panel.objects.filter(elect_id_id=e.elect_id).values('ep_id')

        c = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(cand_status=1) & Q(stud_id_id=sid))
        if c.count() > 0:
            return render(request, 'student/master.html',{'sym':1,'name':t_name})
    return render(request, 'student/master.html',{'name':t_name})

