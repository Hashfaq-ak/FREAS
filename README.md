FREAS (Face Recognition Attendance System)
FREAS is a Django-based application designed for employee attendance tracking using face recognition technology. The system records the in-time and out-time of employees and calculates their daily and monthly salaries based on this data.

Table of Contents
Introduction
Features
Installation
Usage
Contact
Introduction
FREAS (Face Recognition Attendance System) leverages the power of face recognition to streamline the process of tracking employee attendance. Employees can mark their in-time and out-time through the system, and the application automatically calculates their daily and monthly salaries based on the recorded attendance.

Features
Face recognition for accurate attendance marking
Tracks in-time and out-time of employees
Calculates daily and monthly salaries
User-friendly interface for employees and administrators
Secure and scalable architecture using Django framework
Installation
To get started with FREAS, follow these steps:

Clone the repository:

 
 
git clone https://github.com/yourusername/FREAS.git
Navigate to the project directory:

 
 
cd FREAS
Create a virtual environment and activate it:

 
 
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install the dependencies:

 
 
pip install django opencv-python numpy dlib
Apply database migrations:

 
 
python manage.py migrate
Run the development server:

 
 
python manage.py runserver
Access the application in your browser at:

arduino
 
http://127.0.0.1:8000/
Usage
Mark Attendance
Employees can log in to the system.
Use the face recognition feature to mark in-time and out-time.
The system will automatically record these times and calculate the salary.
Administrator Functions
Manage employee records.
View attendance logs.
Oversee salary calculations.
Contact
Your Name - @_ashp.u - muhammedhashfaq.ak@gmail.com

Project Link: https://github.com/Hashfaq-ak/FREAS
