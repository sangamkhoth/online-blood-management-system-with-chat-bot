from rest_framework import serializers
from users.models import User
from core.models import Donor, Hospital, BloodInventory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'address', 'is_donor', 'is_hospital']


class DonorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Donor
        fields = '__all__'


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class BloodInventorySerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    
    class Meta:
        model = BloodInventory
        fields = '__all__'
