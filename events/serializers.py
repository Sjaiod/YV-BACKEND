from rest_framework import serializers
from .models import Event
from members.models import Member

class EventSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), many=True)

    class Meta:
        model = Event  # Ensure the colon is replaced with an equal sign
        fields = '__all__'