from rest_framework import serializers
from ..models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer definition for Message
    object to json.
    """
    #conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        source='conversation'  # Maps conversation_id -> conversation instance
    )

    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'direction', 'content', 'timestamp', 'created_at']