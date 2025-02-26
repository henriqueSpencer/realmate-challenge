from rest_framework import serializers
from ..models import Conversation
from .message import MessageSerializer


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer definition for Conversation
    object to json.
    """
    # without this line, the messages will not be serialized, only the ids would be shown
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'state', 'created_at', 'updated_at', 'messages']