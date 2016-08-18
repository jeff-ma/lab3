from rest_framework import serializers
from .models import Url_Address

class Url_AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Url_Address
        fields = ('id', 'short_url', 'full_url', 'http_status', 'page_title', 'wayback_url', 'timestamp', 'image')
