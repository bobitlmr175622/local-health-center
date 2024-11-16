from django.db import models

# Create your models here.

# User model (for patients, doctors, and admin)
class User(models.Model):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    contact_info = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username


# Patient model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_history = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Not Checked-in")

    def __str__(self):
        return self.user.username


# Appointment model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50, default="Scheduled")

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.date}"


# Invoice model
class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount_due = models.FloatField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.patient.username}"

