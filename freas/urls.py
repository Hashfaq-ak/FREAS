"""
URL configuration for freas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from home import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('employees/', views.employee_list, name='employee_list'),
    path('edit_employee/<str:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<str:employee_id>/', views.delete_employee, name='delete_employee'),
    path('attendance/', views.attendance, name='attendance'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance_out/', views.attendance_out, name='attendance_out'),
    path('mark_out_time_attendance/', views.mark_out_time_attendance, name='mark_out_time_attendance'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('viewbydate/', views.view_attendance_date, name='view-attendance-date'),
    path('viewbyid/', views.view_attendance_employee, name='view-attendance-employee'),
    path('report/', views.salary_form, name='salary_form'),
    path('generate_salary_report/', views.generate_salary_report, name='generate_salary_report'),
]
