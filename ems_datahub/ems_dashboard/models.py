from django.db import models
from django.contrib.auth.models import User

class Call(models.Model):
    TYPE_CHOICES = [
        ('EMS', 'EMS Only'),
        ('EMS/FD', 'EMS/Fire Department'),
        ('FD', 'Fire Department Only'),
    ]
    TRANSPORT_CHOICES = [
        ('Transport', 'Transport'),
        ('Non-Transport', 'Non-Transport'),
        ('N/A', 'N/A (Fire Stand-by, Public Assist, etc.'),
    ]
    date = models.DateField()
    time = models.TimeField()
    type_of_call = models.CharField(max_length=10, choices=TYPE_CHOICES)
    town = models.ForeignKey('Town', on_delete=models.CASCADE)
    responders_count = models.IntegerField()
    medic_intercept = models.BooleanField(default=False)
    intercept_agency = models.ForeignKey('Agency', on_delete=models.SET_NULL, null=True, blank=True)
    transport_type = models.CharField(max_length=15, choices=TRANSPORT_CHOICES)
    cpr_dos = models.BooleanField(default=False)

class Agency(models.Model):
    AGENCY_CHOICES = [
        ('JRMA', 'JRMA'),
        ('PFD', 'Peterborough Fire Department'),
        ('WFD', 'Winchendon Fire Department'),
        ('CEMS', 'Cheshire EMS'),
    ]  
    name = models.CharField(max_length=100, choices=AGENCY_CHOICES)

    def __str__(self):
        return self.get_name_display()

class Town(models.Model):
    TOWN_CHOICES = [
        ('Jaffrey', 'Jaffrey'),
        ('Rindge', 'Rindge'),
        ('Peterborough', 'Peterborough'),
        ('New Ipswich', 'New Ipswich'),
    ]
    name = models.CharField(max_length=100, choices=TOWN_CHOICES)

    def __str__(self):
        return self.get_name_display()

class SavedQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
