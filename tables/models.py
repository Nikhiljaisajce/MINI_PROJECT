from distutils.command.upload import upload
from django.db import models
from django import forms 
# Create your models here.
pv = [
    (0, 'admin'),
    (2, 'department'),
    (3, 'student'),
   
]


class login(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    user_type = models.IntegerField(choices=pv)
    user_id = models.IntegerField()



class department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_email = models.EmailField(max_length=70)
    dept_phone = models.CharField(max_length=20)


class course(models.Model):
    course_id = models.AutoField(primary_key=True)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=100)
    duration = models.IntegerField()

    
class student(models.Model):
    stud_id = models.AutoField(primary_key=True)
    stud_fname = models.CharField(max_length=100)
    stud_mname = models.CharField(null=True,max_length=100)
    stud_lname = models.CharField(max_length=100)
    stud_dob = models.DateField(null=True)
    stud_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    stud_email = models.EmailField(max_length=70)
    stud_mob = models.CharField(null=True,max_length=11)
    stud_course_id = models.ForeignKey(course, on_delete=models.CASCADE)
    stud_start_date = models.DateField()
    stud_end_date = models.DateField()
  

class election(models.Model):
    elect_id=models.AutoField(primary_key=True)
    elect_date=models.DateField()
    elect_nomi_start_date=models.DateField()
    elect_nomi_end_date=models.DateField()
    elect_nomi_withdrawal_end_date=models.DateField()
    elect_status = models.IntegerField(default=0)

class panel(models.Model):
    panel_id=models.AutoField(primary_key=True)
    panel_post=models.CharField(max_length=100)
    panel_type=models.IntegerField(default=0, choices=[(0, 'General'), (1, 'female')])
    panel_status=models.IntegerField(default=1, choices=[(0, 'inactive'), (1, 'active')])
    panel_year=models.IntegerField(default=0, choices=[(0, 'all'), (1, '1st year'), (2, '2nd year'), (3, '3rd year'), (4, '4th year')])
    panel_votes = models.IntegerField(default=1)

class panel_specific(models.Model):
    specific_id=models.AutoField(primary_key=True)
    panel_id=models.ForeignKey(panel,on_delete=models.CASCADE)
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)


class election_panel(models.Model):
    ep_id=models.AutoField(primary_key=True)
    elect_id=models.ForeignKey(election,on_delete=models.CASCADE)
    panel_id=models.ForeignKey(panel,on_delete=models.CASCADE)
 
class tbl_Employee(models.Model):    
  #  Id = models.IntegerField()
    Empcode = models.CharField(max_length=10, default='')
    firstName = models.CharField(max_length=150,null=True)
    middleName = models.CharField(max_length=100,null=True)    
    lastName = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=30,null=True)
    phoneNo = models.CharField(max_length=12, default='',null=True)
    address = models.CharField(max_length=500, default='',null=True) 
    exprience = models.CharField(max_length=50, default='',null=True)        
    DOB = models.DateField(null=True, blank=True)   
    gender = models.CharField(max_length=10, default='',null=True)
    qualification = models.CharField(max_length=50,default='',null=True)   
     
      
 
    def __str__(self):
        return self.firstName
                 
    objects = models.Manager()