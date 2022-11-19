from django import forms
 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field
 
from .models import tbl_Employee
 
class EmployeeRegistration(forms.ModelForm):
    class Meta:
        model = tbl_Employee
        fields =[ 'Empcode','firstName','middleName','lastName','email','phoneNo' ,'address','exprience',
                  'DOB','gender','qualification'
        ] 