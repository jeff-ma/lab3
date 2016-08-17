from rest_framework import serializers
from .models import Url_Address

class Url_AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Url_Address
        fields = '__all__'
