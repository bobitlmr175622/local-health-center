
# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Patient, Appointment, Invoice
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser

# User login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid credentials.")
    return render(request, 'management/login.html')


# Patient registration view
def register_patient(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        contact_info = request.POST['contact_info']
        
        user = User.objects.create(username=username, password=password, role="patient", name=name, contact_info=contact_info)
        Patient.objects.create(user=user)  # Automatically create a Patient entry
        return redirect('login')
    return render(request, 'management/register_patient.html')


# Dashboard view (after login)
def dashboard(request):
    if request.user.role == 'patient':
        # Get patient's upcoming appointments
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient, status="Scheduled")
        return render(request, 'management/patient_dashboard.html', {'appointments': appointments})
    
    elif request.user.role == 'doctor':
        # Get doctor's upcoming appointments
        doctor = User.objects.get(username=request.user.username)
        appointments = Appointment.objects.filter(doctor=doctor, status="Scheduled")
        return render(request, 'management/doctor_dashboard.html', {'appointments': appointments})
    
    elif request.user.role == 'admin':
        # Admin view for managing users
        users = User.objects.all()
        return render(request, 'management/admin_dashboard.html', {'users': users})
    
    return HttpResponse("Invalid role")


# Schedule appointment view
def schedule_appointment(request, patient_id):
    if request.method == "POST":
        doctor_id = request.POST['doctor_id']
        date = request.POST['date']
        reason = request.POST['reason']

        doctor = User.objects.get(id=doctor_id)
        patient = Patient.objects.get(id=patient_id)
        Appointment.objects.create(patient=patient, doctor=doctor, date=date, reason=reason)
        
        return redirect('dashboard')
    return render(request, 'management/schedule_appointment.html')


# Check-in patient view
def check_in_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.status = "Checked-in"
    patient.save()
    return redirect('dashboard')


# Generate invoice view
def generate_invoice(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    total_due = calculate_invoice_amount(patient)
    invoice = Invoice.objects.create(patient=patient, amount_due=total_due)
    return redirect('dashboard')


# Helper function to calculate invoice amount (sum of appointment costs)
def calculate_invoice_amount(patient):
    appointments = Appointment.objects.filter(patient=patient, status="Completed")
    total_amount = sum([appointment.cost for appointment in appointments])
    return total_amount

