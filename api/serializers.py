from rest_framework import serializers
from .models import BoatStatus

class BoatStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoatStatus
        fields = '__all__'  # หรือระบุฟิลด์ที่ต้องการได้ เช่น ['name', 'lat', 'lon', ...]
        read_only_fields = ['id', 'timestamp']
