from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# Create your views here.
from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.http import JsonResponse
from tables.models import *
from django.db.models import Q
# for otp
import math, random

def getName(request):
    t_did = request.session['id']
    t_d = department.objects.get(dept_id=t_did)
    t_name = t_d.dept_name
    return  t_name

def home(request):
    return render(request,'department/master.html')

    # keys = request.session.keys()
    # if 'id' not in keys:
    #     messages.success(request, "Session Expired! Please Login Again")
    #     return redirect('http://127.0.0.1:8000/home/login')

    # t_name = getName(request)
    # return render(request, 'department/master.html',{'name':t_name})


def addstud(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    # obj = election.objects.filter(elect_status=0)
    # if obj.count() >0:
    #     messages.success(request, "Access denied due to Election!")
        return redirect('http://127.0.0.1:8000/home/department/')

    did = request.session['id']
    c = course.objects.filter(dept_id_id=did)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        gen = request.POST.get('gen')
        co = request.POST.get('cr')
        sdate = request.POST.get('startdate')
        edate = request.POST.get('enddate')
        email = request.POST.get('email')
        s = student.objects.filter(stud_email=email)
        if s.count() == 0:
            s = student(stud_fname=fname, stud_mname=mname, stud_lname=lname, stud_gender=gen, stud_email=email,
                        stud_start_date=sdate, stud_end_date=edate, stud_course_id_id=co)
            s.save()
            user = "stud" + str(s.stud_id)
            pwd = "stud" + str(s.stud_id)
            print(s.stud_id)
            l = login(username=user, password=pwd, user_type=3, user_id=s.stud_id)
            l.save()
            subject = 'College_Election - Student Login Details'
            if mname == '':
                message = 'Dear ' + fname + ' ' + lname + '\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd
            else:
                message = 'Dear ' + fname + ' ' + mname + ' ' + lname + '\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd

            message += '\nNote: Please use forgot password option to change your password!'
            recepient = str(email)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            messages.success(request, "Student Details Saved")
    t_name = getName(request)
    return render(request, 'department/StudAdd.html', {'courses': c, 'name':t_name})

def validate_addstud(request):
    email = request.GET.get('email')
    s = student.objects.filter(stud_email=email)
    dmail_status = False
    if s.count() > 0:
        dmail_status = True
    data = {
        'dmail_status': dmail_status
    }
    return JsonResponse(data)


def deptedit(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    did = request.session['id']
    d = department.objects.filter(dept_id=did)
    t_name = getName(request)
    if request.method == 'POST':
        keys = request.session.keys()
        postKeys = request.POST.keys()
        if 'oldOtp' in postKeys:
            if 'mobOtp' in keys:
                if request.session['mobOtp'] != request.POST['oldOtp']:
                    messages.success(request, "OTP Verification Failed!")
                    return render(request, 'department/DeptEdit.html', {'dept': d, 'name':t_name})

        if 'oldOtp' in postKeys:
            if 'oldMailOtp' in keys:
                if request.session['oldMailOtp'] != request.POST['oldOtp']:
                    messages.success(request, "OTP Verification Failed!")
                    return render(request, 'department/DeptEdit.html', {'dept': d,'name':t_name})
        if 'newOtp' in postKeys:
            if 'newMailOtp' in keys:
                if request.session['newMailOtp'] != request.POST['newOtp']:
                    messages.success(request, "OTP Verification Failed!")
                    return render(request, 'department/DeptEdit.html', {'dept': d, 'name':t_name})
        dmail = request.POST['dmail']
        dmob = request.POST['txtPhone']
        department.objects.filter(dept_id=did).update(dept_email=dmail, dept_phone=dmob)
        messages.success(request, "Modifications Saved")

    return render(request, 'department/DeptEdit.html', {'dept': d,'name':t_name})


def validate_dept_edit(request):
    dmail = request.GET.get('dmail')
    dmob = request.GET.get('dmob')
    did = request.session['id']
    for key in list(request.session.keys()):
        if  key.startswith("oldMailOtp"):  # skip keys set by the django system
            del request.session[key]
        if  key.startswith("newMailOtp"):  # skip keys set by the django system
            del request.session[key]
        if  key.startswith("mobOtp"):  # skip keys set by the django system
            del request.session[key]
    d = department.objects.filter(dept_id=did)

    dmobStatus = False
    dmailStatus = False
    dexist = False

    d1 = department.objects.filter(~Q(dept_id=did))
    for j in d1:
            if j.dept_email == dmail:
                dexist = True
                data = {
                    'dmail_status': dmailStatus,
                    'dmob_status': dmobStatus,
                    'dexist': dexist
                }
                return JsonResponse(data)

    if d.count() > 0:
        for obj in d:
            if (dmail == obj.dept_email) and (dmob == obj.dept_phone):
                dexist = True
                data = {
                    'dmail_status': dmailStatus,
                    'dmob_status': dmobStatus,
                    'dexist' : dexist
                }
                return JsonResponse(data)

            if (dmail != obj.dept_email) and (dmob != obj.dept_phone):
                oldMailOtp = OTPgenerator()
                newMailOtp = OTPgenerator()
                sendOtpToMAil(obj.dept_email, oldMailOtp, 'old')
                sendOtpToMAil(dmail, newMailOtp, 'new')
                request.session['newMailOtp'] = newMailOtp
                request.session['oldMailOtp'] = oldMailOtp
                dmailStatus = True
                dmobStatus = True
            elif dmail != obj.dept_email:  # new mail so otp need to old and new mail
                oldMailOtp = OTPgenerator()
                newMailOtp = OTPgenerator()
                sendOtpToMAil(obj.dept_email,oldMailOtp,'old')
                sendOtpToMAil(dmail, newMailOtp,'new')
                request.session['newMailOtp'] = newMailOtp
                request.session['oldMailOtp'] = oldMailOtp
                dmailStatus = True


            elif dmob != obj.dept_phone:  # new mobile so otp to old mail
                mobOtp = OTPgenerator()
                sendOtpToMAil(obj.dept_email, mobOtp, 'mob')
                request.session['mobOtp'] = mobOtp
                dmobStatus = True

            data = {
                'dmail_status' : dmailStatus,
                'dmob_status'  : dmobStatus
            }
            break
        return  JsonResponse(data)





def sendOtpToMAil(mailAddr, otp,msg):
    subject = 'College_Election - OTP for Department Edit Verification'
    if msg=='old':
        message = 'Hello,\nYour One Time Password for changing '+str(mailAddr)+' to new Mail id is\n'+ str(otp)
    if msg=='new':
        message = 'Hello,\nYour One Time Password for activating ' + str(mailAddr) + ' is\n' + str(otp)
    if msg=='mob':
        message = 'Hello,\nYour One Time Password for changing mobile number is \n'+ str(otp)
    mailAddr = str(mailAddr)
    recepient = str(mailAddr)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
