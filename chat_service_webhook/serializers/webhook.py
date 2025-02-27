from rest_framework import serializers
from .message import MessageSerializer
from .conversation import ConversationSerializer
from ..models import Conversation, Message


class WebhookSerializer(serializers.Serializer):
    """
    Validate and structure the data received by the webhook.
    """
    EVENT_TYPES = ["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"]
    type = serializers.ChoiceField(choices=EVENT_TYPES)
    timestamp = serializers.DateTimeField()
    data = serializers.JSONField()

    def validate_data(self, value):
        """
        Validates the 'data' field based on the event type.

        This method is called automatically by `is_valid()` in Django REST Framework
        when validating the serializer.

        Parameters:
          value (dict): The `data` dictionary containing event-specific information.

        Returns:
          dict: The validated data.
        """
        event_type = self.initial_data.get("type")

        if event_type == "NEW_CONVERSATION":
            if "id" not in value:
                raise serializers.ValidationError({"id": "Conversation ID is required."})

        elif event_type == "NEW_MESSAGE":
            # Validate if it has the required fields
            required_fields = ["id", "direction", "content", "conversation_id"]
            missing_fields = [field for field in required_fields if field not in value]
            if missing_fields:
                raise serializers.ValidationError({field: "This field is required." for field in missing_fields})

            # Validate direction field if it is one of the options expected
            if value.get("direction") not in ["SENT", "RECEIVED"]:
                raise serializers.ValidationError(
                    {"direction": "Invalid message direction. Must be 'SENT' or 'RECEIVED'."})

        elif event_type == "CLOSE_CONVERSATION":
            if "id" not in value:
                raise serializers.ValidationError({"id": "Conversation ID is required."})

        return value

    def to_representation(self, instance):
        """
        Converts the instance into a serializable dictionary format.

        This method overrides `to_representation()` from the parent `Serializer` class.
        It is called automatically by Django REST Framework when transforming a serializer
        instance into a JSON response.

        Parameters:
            instance (dict): The validated data containing `type`, `timestamp`, and `data`.

        Returns:
            dict: A formatted dictionary representation of the event.
        """
        event_type = instance.get("type")
        data = instance.get("data")

        if event_type == "NEW_CONVERSATION":
            conversation = Conversation.objects.filter(id=data.get("id")).first()
            return {
                "type": event_type,
                "timestamp": instance.get("timestamp"),
                "data": ConversationSerializer(conversation).data if conversation else data
            }

        elif event_type == "NEW_MESSAGE":
            message = Message.objects.filter(id=data.get("id")).first()
            return {
                "type": event_type,
                "timestamp": instance.get("timestamp"),
                "data": MessageSerializer(message).data if message else data
            }

        elif event_type == "CLOSE_CONVERSATION":
            return {
                "type": event_type,
                "timestamp": instance.get("timestamp"),
                "data": {"id": data.get("id")}
            }

        return super().to_representation(instance)


