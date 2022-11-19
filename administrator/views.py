import datetime
from django.shortcuts import render,redirect
from tables.models import *
from django.db.models import Q, Count
from django.http import HttpResponse
from django.contrib import messages
#for email
import datetime
from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
#for ajax response
from django.http import  JsonResponse, HttpResponseRedirect
# Create your views here.
def home(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    return render(request,'administrator/master.html')

def paneladd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    # e=election.objects.filter(elect_status=0)
    # if e.count()>0:
        messages.success(request, "Cannot add panel, because an election is declared")
        return redirect('http://127.0.0.1:8000/home/admin')


    cs=course.objects.all()
    if request.method=='POST':
        pname=request.POST.get('pname')
        ptype=int(request.POST.get('ptype'))
        #pstatus=int(request.POST.get('pstatus'))
        yob=int(request.POST.get('yob'))
        cr=request.POST.getlist('checks')
        p=panel(panel_post=pname,panel_type=ptype,panel_year=yob)
        p.save()
        if len(cr)>0:
            for c in cr:
                ps=panel_specific(course_id_id=c,panel_id_id=p.panel_id)
                ps.save()

    #     messages.success(request, "Panel Details Saved Successfully")
    # obj = panel.objects.all()
    # if obj.count()==0:
        return render(request,'administrator/paneladd.html',{'courses':cs})
    return render(request, 'administrator/paneladd.html')


def paneledit(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')     

    p = panel.objects.all()
    if p.count()==0:
        messages.success(request, "Panels not found!")
        return redirect('http://127.0.0.1:8000/home/admin')

    e = election.objects.filter(elect_status=0)
    if e.count() > 0:
        messages.success(request, "Cannot add panel, because an election is declared")
        return redirect('http://127.0.0.1:8000/home/admin')

    p = panel.objects.all()
    p_s = panel_specific.objects.all()
    c = course.objects.all()
    p_s_id = []
    c_id = []
    for c1 in c:
        c_id.append(c1.course_id)
    for s1 in p_s:
        p_s_id.append(s1.panel_id.panel_id) #id's of panel in panel_specific
    if request.method=='POST':
        panelid = request.POST.get('approve')
        ptype = int(request.POST.get('ptype'+str(panelid)))
        yob = int(request.POST.get('yob'+str(panelid)))
        cr = request.POST.getlist('checks'+str(panelid))

        if len(cr)==0:
            if int(panelid) in p_s_id:   #delete all entries of panel from panel_specific
                obj = panel_specific.objects.filter(panel_id=panelid).delete()
        else:
            obj = panel_specific.objects.filter(panel_id=panelid).delete()
            for c1 in cr:
                ps=panel_specific(course_id_id=c1,panel_id_id=panelid)
                ps.save()
        obj = panel.objects.filter(panel_id=panelid).update(panel_type=ptype,panel_year=yob)

        messages.success(request, "Panel Details Edited Successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'administrator/paneledit.html')


def deptadd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    # e = election.objects.filter(elect_status=0)
    # if e.count() > 0:
    #     messages.success(request, "Cannot add panel, because an election is declared")
        return redirect('http://127.0.0.1:8000/home/admin')


    if request.method=='POST':
        dname = request.POST.get('dname')
        dmail = request.POST.get('dmail')
        dphone = request.POST.get('txtPhone')
        s = department.objects.filter(dept_name=dname)
        dname_status= dmail_status = False
        if s.count() > 0:
            dname_status = True
        s = department.objects.filter(dept_email=dmail)
        if s.count() > 0:
            dmail_status = True
        if not(dmail_status) or not(dname_status):
            d=department(dept_name=dname,dept_email=dmail,dept_phone=dphone)
            d.save()
            user="dept"+str(d.dept_id)
            pwd="dept"+str(d.dept_id)
            l=login(username=user,password=pwd,user_type=2,user_id=d.dept_id)
            l.save()
            #send username and password to mail
            subject = 'College_Election - '+dname+' Department Login Details'
            message = 'Hello,\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: '+user+'\nPassword: '+pwd
            message += '\nNote: Please use forgot password option to change your password!'
            recepient = str(dmail)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            messages.success(request,"Department Registration Success")
        else:
            messages.success(request, "Data Repetition Found!")
    obj = department.objects.all()
    if obj.count() ==0:
        return render(request,'administrator/deptadd.html')

    return render(request, 'administrator/deptadd.html',{'d':obj})





def validate_dept(request):
    dname = request.GET.get('dname')
    dmail = request.GET.get('dmail')
    s = department.objects.filter(dept_name=dname)
    dname_status = False
    dmail_status = False
    if s.count() > 0:
        dname_status =True
    s = department.objects.filter(dept_email=dmail)
    if s.count() > 0:
        dmail_status = True
    data = {
        'dname_status' :dname_status,
        'dmail_status' :dmail_status
    }
    return JsonResponse(data)



def deptReport(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = department.objects.all()
    c = course.objects.all()
    if obj.count()==0:
        messages.success(request, "Department list is empty!")
        return redirect('http://127.0.0.1:8000/home/admin')

    return render(request, 'administrator/deptrpt.html',{'dept': obj, 'c': c})


def electionadd(request):
    return render(request,'electionadd.html')

   
   
def postpone(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    # if request.method == 'POST':
    #     dateval = request.POST['newelectDt']
    #     election.objects.filter(elect_status=0, elect_date__gt=datetime.date.today()).update(elect_date=dateval)
    #     messages.success(request, "Election postponed to "+dateval)
    #     return redirect('http://127.0.0.1:8000/home/admin')


    # e=election.objects.filter(elect_status=0)
    # if e.count()==0:
    #     messages.success(request, "No election to postpone")
    #     return redirect('http://127.0.0.1:8000/home/admin')

    # if(e[0].elect_date<=datetime.date.today()):
    #     messages.success(request, "can't postpone now")
    #     return redirect('http://127.0.0.1:8000/home/admin')


    # min=str(e[0].elect_date+datetime.timedelta(days=1))
    return render(request,'administrator/postpone.html')

