from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'department', 'photo', 'designation', 'salary', 'date_of_birth']


from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


# from django.contrib.admin.widgets import AdminDateWidget


class DateForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))


class UsernameAndDateForm(forms.Form):
    username = forms.CharField(max_length=30)
    date_from = forms.DateField(
        widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    date_to = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))


from django import forms

class EmployeeAttendanceForm(forms.Form):
    employee_name = forms.CharField(max_length=100, label='Employee Name')
    date_from = forms.DateField(label='From Date', widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label='To Date', widget=forms.DateInput(attrs={'type': 'date'}))


class SalaryReportForm(forms.Form):
    employee_name = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label="Select Employee")
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=1900, max_value=2100)
