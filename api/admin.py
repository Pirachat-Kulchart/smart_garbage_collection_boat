from django.contrib import admin

from .models import BoatStatus, Profile, Vessel, SensorData

# User Profile
admin.site.register(Profile)

# Vessel and Boat Status
admin.site.register(SensorData)
admin.site.register(BoatStatus)
admin.site.register(Vessel)
