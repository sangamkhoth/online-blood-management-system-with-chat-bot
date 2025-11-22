from django.db import models
from django.conf import settings

class Donor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    last_donated = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class BloodInventory(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)

    blood_group = models.CharField(max_length=5)
    units_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.blood_group} ({self.units_available} units)"
