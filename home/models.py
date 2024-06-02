from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.db import models

# myapp/models.py
from django.db import models

from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employee_photos', null=True, blank=True)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_birth = models.DateField()
    face_encoding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name
# myapp/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Attendance(models.Model):
    attendance_number = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    month = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f"Attendance for Employee ID: {self.employee.employee_id}, Date: {self.date}"
