from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import WebhookSerializer
from .handlers import create_conversation, close_conversation, add_message
from rest_framework.exceptions import ValidationError  # Import from DRF
from django.core.exceptions import ObjectDoesNotExist  # Import from Django

from .serializers import ConversationSerializer
from .models import Conversation
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def webhook(request):
    """
    Process webhook events and trigger the appropriate actions based on the event type.

    Parameters:
        request (Request): A  DRF(Django REST Framework Request object) containing the webhook payload.

    Returns:
        Response: A DRF Response object with a success or error message and appropriate HTTP status.
    """
    try:
        serializer = WebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        event_type = serializer.validated_data['type']
        timestamp = serializer.validated_data['timestamp']
        data = serializer.validated_data['data']

        handlers = {
            "NEW_CONVERSATION": lambda: create_conversation(data.get('id')),
            "NEW_MESSAGE": lambda: add_message(data, timestamp),
            "CLOSE_CONVERSATION": lambda: close_conversation(data.get('id'))
        }

        # Don't need to check if the event type is in the handlers dictionary,
        # because it's already validated in the serializer
        response_data, response_status = handlers[event_type]()
        return Response(response_data, status=response_status)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return Response(
            {"error": "Internal server error", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




class ConversationDetailView(APIView):
    """API view to retrieve a single conversation by its ID."""
    def get(self, request, conversation_id):
        """
        Handle GET request to retrieve a specific conversation.

        Parameters:
            request (Request): The Django REST Framework request object.
            conversation_id (str): The unique identifier of the conversation.

        Returns:
            Response: A JSON response containing:
                - If successful: The serialized conversation data (`200 OK`).
                - If conversation not found: `404 Not Found`.
                - If an unexpected error occurs: `400 Bad Request`.
        """
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Failed to retrieve conversation", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )