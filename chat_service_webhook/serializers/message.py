from rest_framework import serializers
from ..models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer definition for Message
    object to json.
    """
    class Meta:
        model = Message
        fields = ['id', 'direction', 'content', 'timestamp']