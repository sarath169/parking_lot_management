from rest_framework import serializers
from user_dash.models import Vehicle

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('number',)
        extra_kwargs = {'number': {'required': True}}

class ExitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('number',)
        extra_kwargs = {'number': {'required': True}}
