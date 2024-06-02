from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from datetime import datetime, date
from .forms import EmployeeForm, SalaryReportForm, DateForm, EmployeeAttendanceForm
from .models import Employee, Attendance
from django.utils import timezone
import base64
import numpy as np
import cv2
import face_recognition
import os
from django.db.models import Sum

def home(request):
    return render(request, 'home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'admin_login.html')
    return render(request, 'admin_login.html')

@login_required
@staff_member_required
def admin_home(request):
    is_admin = request.user.is_staff  # Check if the user is an admin
    return render(request, 'admin_home.html', {'is_admin': is_admin})

@login_required
@staff_member_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('admin_home')
        else:
            messages.error(request, 'Error adding employee. Please check the form.')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

@login_required
@staff_member_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
@staff_member_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Redirect to employee list page
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})

@login_required
@staff_member_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    # Render confirmation template for GET request
    return render(request, 'confirm_delete.html', {'employee': employee})

@login_required
@staff_member_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
@staff_member_required
def reports(request):
    # Query to get the total number of employees
    total_num_of_emp = Employee.objects.count()

    # Query to get the number of employees present today
    today = date.today()
    emp_present_today = Attendance.objects.filter(date=today).values('employee').distinct().count()

    # Pass the total number of employees and employees present today to the template
    return render(request, 'reports.html',
                  {'total_num_of_emp': total_num_of_emp, 'emp_present_today': emp_present_today})

@login_required
@staff_member_required
def view_attendance_date(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            # Query your Attendance model to get data for the selected date
            attendance_data = Attendance.objects.filter(date=selected_date)
            context = {
                'form': form,
                'qs': attendance_data,
            }
            return render(request, 'view_attendance_date.html', context)
    else:
        form = DateForm()
    context = {
        'form': form,
    }
    return render(request, 'view_attendance_date.html', context)

@login_required
@staff_member_required
def view_attendance_employee(request):
    if request.method == 'POST':
        form = EmployeeAttendanceForm(request.POST)
        if form.is_valid():
            employee_name = form.cleaned_data['employee_name']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            # Query attendance records based on employee name and date range
            attendance_records = Attendance.objects.filter(
                employee__name=employee_name,
                date__range=[date_from, date_to]
            )

            if attendance_records:
                context = {
                    'form': form,
                    'qs': attendance_records,
                    'messages': None  # No messages to display
                }
            else:
                context = {
                    'form': form,
                    'qs': None,  # No attendance records found
                    'messages': "No attendance records found for this employee within the specified date range."
                }

            return render(request, 'view_attendance_employee.html', context)
    else:
        form = EmployeeAttendanceForm()

    context = {
        'form': form,
        'qs': None,  # No query result initially
        'messages': None  # No messages initially
    }
    return render(request, 'view_attendance_employee.html', context)

def attendance(request):
    return render(request, 'attendance.html')

def mark_attendance(request):
    if request.method == 'POST':
        try:
            # Get the image data from the request
            image_data = request.POST.get('employee_photo')
            if image_data is None:
                return JsonResponse({'error': 'No image data provided'}, status=400)

            # Decode the base64 encoded image data
            img_bytes = base64.b64decode(image_data.split(',')[1])

            # Convert the image data to numpy array
            nparr = np.frombuffer(img_bytes, dtype=np.uint8)

            # Decode the image using OpenCV
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Find faces in the image
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                return JsonResponse({'error': 'No faces detected in the image'}, status=400)

            # Encode the faces found in the image
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Load employee photos from disk and compare face encodings
            for filename in os.listdir('media/employee_photos'):
                employee_id = os.path.splitext(filename)[0]  # Extract employee ID from filename
                employee = Employee.objects.filter(employee_id=employee_id).first()
                if employee is not None:
                    employee_image = face_recognition.load_image_file(os.path.join('media/employee_photos', filename))
                    employee_face_encoding = face_recognition.face_encodings(employee_image)
                    if len(employee_face_encoding) > 0:
                        employee_face_encoding = employee_face_encoding[0]

                        # Compare face encodings with encodings of faces in employee photos
                        for face_encoding in face_encodings:
                            match = face_recognition.compare_faces([employee_face_encoding], face_encoding)
                            if match[0]:
                                # If a match is found, record attendance
                                current_time = timezone.now()
                                # Check if the employee has an existing IN attendance record for today
                                existing_attendance = Attendance.objects.filter(employee=employee, date=current_time.date()).first()
                                if existing_attendance:
                                    return JsonResponse({'error': 'Attendance already recorded for today'})
                                else:
                                    # If no attendance record exists for today, create a new one
                                    Attendance.objects.create(employee=employee, date=current_time.date(), start_time=current_time, end_time=None, month=current_time.month)
                                break  # Exit the loop if a match is found
            response_data = {'message': 'Attendance marked successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def attendance_out(request):
    return render(request,'attendance_out.html')

def mark_out_time_attendance(request):
    if request.method == 'POST':
        try:
            # Get the image data from the request
            image_data = request.POST.get('employee_photo')
            if image_data is None:
                return JsonResponse({'error': 'No image data provided'}, status=400)

            # Decode the base64 encoded image data
            img_bytes = base64.b64decode(image_data.split(',')[1])

            # Convert the image data to numpy array
            nparr = np.frombuffer(img_bytes, dtype=np.uint8)

            # Decode the image using OpenCV
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Find faces in the image
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                return JsonResponse({'error': 'No faces detected in the image'}, status=400)

            # Encode the faces found in the image
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Load employee photos from disk and compare face encodings
            for filename in os.listdir('media/employee_photos'):
                employee_id = os.path.splitext(filename)[0]  # Extract employee ID from filename
                employee = Employee.objects.filter(employee_id=employee_id).first()
                if employee is not None:
                    employee_image = face_recognition.load_image_file(os.path.join('media/employee_photos', filename))
                    employee_face_encoding = face_recognition.face_encodings(employee_image)
                    if len(employee_face_encoding) > 0:
                        employee_face_encoding = employee_face_encoding[0]

                        # Compare face encodings with encodings of faces in employee photos
                        for face_encoding in face_encodings:
                            match = face_recognition.compare_faces([employee_face_encoding], face_encoding)
                            if match[0]:
                                # If a match is found, record out-time attendance
                                current_time = timezone.now()
                                # Check if the employee has an existing IN attendance record for today
                                existing_attendance = Attendance.objects.filter(employee=employee, date=current_time.date()).first()
                                if existing_attendance:
                                    # If an IN attendance record exists, update the end time and hours worked
                                    existing_attendance.end_time = current_time
                                    existing_attendance.hours = (current_time - existing_attendance.start_time).total_seconds() / 3600
                                    existing_attendance.save()
                                    response_data = {'message': 'Out-time attendance recorded successfully'}
                                    return JsonResponse(response_data)
                                else:
                                    # If no IN attendance record exists, return error
                                    return JsonResponse({'error': 'No in-time attendance recorded for this employee today'}, status=400)
            # If no match found for the employee
            return JsonResponse({'error': 'No matching employee found'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def calculate_daily_salary(monthly_salary, hours_worked):
    # Assuming monthly salary is based on a 40-hour work week
    weekly_hours = 40
    daily_salary = (monthly_salary / 4) / weekly_hours * hours_worked
    return round(daily_salary, 2)
@login_required
@staff_member_required
def generate_salary_report(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        month = request.POST.get('month')
        year = request.POST.get('year')

        # Retrieve the employee object
        employee = Employee.objects.get(employee_id=employee_id)

        # Retrieve the monthly salary of the employee
        monthly_salary = employee.salary

        # Retrieve all attendance records for the selected month and year
        attendance_records = Attendance.objects.filter(
            employee=employee,
            date__month=month,
            date__year=year
        )

        salary_report_data = []
        total_salary = 0

        # Calculate daily salary for each attendance record
        for record in attendance_records:
            daily_salary = calculate_daily_salary(monthly_salary, record.hours)
            salary_report_data.append({
                'date': record.date,
                'hours_worked': record.hours,
                'daily_salary': daily_salary,
            })
            total_salary += daily_salary

        context = {
            'employee': employee,
            'month': month,
            'year': year,
            'salary_report_data': salary_report_data,
            'total_salary': round(total_salary, 2),
        }

        return render(request, 'salary_report.html', context)
    else:
        return render(request, 'generate_salary_report.html')

@login_required
@staff_member_required
def salary_form(request):
    form = SalaryReportForm()
    return render(request, 'generate_salary_report.html', {'form': form})
