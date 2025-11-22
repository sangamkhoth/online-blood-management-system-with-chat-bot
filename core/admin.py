from django.contrib import admin
from .models import Donor, Hospital, BloodInventory

admin.site.register(Donor)
admin.site.register(Hospital)
admin.site.register(BloodInventory)
