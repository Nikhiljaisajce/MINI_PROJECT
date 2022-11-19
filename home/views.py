from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from tables.models import *
from django.db.models import Q, Count
from django.contrib import messages
import datetime, math, random
from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from matplotlib import pyplot as plt

from django.http import HttpResponse


# Create your views here.
def home(request):
    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]

    # e = election.objects.filter(elect_status=0)
    # menuHide = 0
    # elect_status = 0
    # if e.count() == 0:
    #     menuHide = 1
    # elif e[0].elect_date != datetime.date.today():
    #     menuHide = 1
    # if e.count() != 0:
    #     elect_status = 1
        return render(request, 'home/master.html/',)
    return render(request, 'home/master.html/',)


def Login(request):
    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pass']
        u = login.objects.filter(Q(username=uname) & Q(password=pwd))
        if u:
            request.session['id'] = u[0].user_id
            if u[0].user_type == 0:
                return redirect('http://127.0.0.1:8000/home/admin/')
            elif u[0].user_type == 1:
                s = staff.objects.get(staff_id=request.session['id'])
                if s.staff_status==0:
                    messages.success(request, "Access Denied. Your account is deactivated.")
                    return redirect('http://127.0.0.1:8000/home/login/')
                else:
                    return redirect('http://127.0.0.1:8000/home/staff/')
            elif u[0].user_type == 2:
                return redirect('http://127.0.0.1:8000/home/department/')
            elif u[0].user_type == 3:
                s = student.objects.get(stud_id=request.session['id'])
                if s.stud_end_date < datetime.date.today():
                    messages.success(request, "Access Denied. You are not studying in collage currently")
                    return redirect('http://127.0.0.1:8000/home/login/')
                else:
                    return redirect('http://127.0.0.1:8000/home/student/')
            else:
                return redirect('http://127.0.0.1:8000/home/party/')

        else:
            messages.success(request, "Invalid Username or Password")

    # e = election.objects.filter(elect_status=0)
    # menuHide = 0
    # if e.count() == 0:
    #     menuHide = 1
    # elif e[0].elect_date != datetime.date.today():
    #     menuHide = 1
    return render(request, 'home/login.html/',)




  
def resetPass(request):

    if request.method=='POST':
        uname = request.POST['uname']
        mail = request.POST['mail']
        loginObj = login.objects.filter(username=uname)
        if loginObj.count()==0:
            messages.success(request,"Incorrect Data")
        elif loginObj.count() ==1:
            obj = loginObj.get()
            request.session['uname'] = obj.username
            if obj.user_type == 1:
                userobj = staff.objects.get(staff_id=obj.user_id)
                if mail == userobj.staff_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")
            if obj.user_type == 2:
                userobj = department.objects.get(dept_id=obj.user_id)
                if mail == userobj.dept_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")
            if obj.user_type == 3:
                userobj = student.objects.get(stud_id=obj.user_id)
                if mail == userobj.stud_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")
            if obj.user_type == 4:
                userobj = party.objects.get(party_id=obj.user_id)
                if mail == userobj.party_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")

    # e = election.objects.filter(elect_status=0)
    # menuHide = 0
    # if e.count() == 0:
    #     menuHide = 1
    # elif e[0].elect_date != datetime.date.today():
    #     menuHide = 1
    return render(request,'home/resetPassword.html')


def confirmPass(request):
    keys = request.session.keys()
    if 'otp' not in keys:
        messages.success(request, "Session Expired!")
        return redirect('http://127.0.0.1:8000/home/login')

    if request.method=='POST':
        otp = request.session['otp']
        uotp = request.POST['otp']
        upwd = request.POST['pwd']
        upwd1 = request.POST['pwd1']

        if otp != uotp :
            messages.success(request, "Incorrect OTP!")
        if upwd != upwd1:
            messages.success(request, "Password not match")
        if otp == uotp and upwd == upwd1:
            uname = request.session['uname']
            login.objects.filter(username=uname).update(password=upwd)
            messages.success(request, "Password Changed")
            del request.session['otp']
            del request.session['uname']
            return redirect('http://127.0.0.1:8000/home/login')

    e = election.objects.filter(elect_status=0)
    menuHide = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1
    return render(request,'home/confirmPassword.html',{'menuHide':menuHide})


def OTPgenerator():
    digits_in_otp = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(digits_in_otp)
    for i in range(6):
        OTP += digits_in_otp[math.floor(random.random() * length)]

    print(OTP)
    return OTP

def sendOtpToMAil(mailAddr, otp):
    subject = 'College_Election - OTP for Staff RESET PASSWORD'
    message = 'Hello,\nYour One Time Password for changing password is \n' + str(otp)
    recepient = str(mailAddr)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

