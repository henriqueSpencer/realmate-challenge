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
from django.shortcuts import render
from celery import shared_task
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # Disabled CSRF protection for this view
@api_view(['POST'])
def webhook(request):
    """
    Receives webhook events and delegates processing to Celery.

    This function validates the received payload and enqueues it as a Celery task,
    ensuring asynchronous processing without delaying the API response.

    Parameters:
        request (Request): A  DRF(Django REST Framework Request object) containing the webhook payload.

    Returns:
        Response: A DRF Response object containing:
            - A confirmation message and the Celery task ID if the request is valid.
            - An error message if the request data is invalid.
    """
    try:
        serializer = WebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        task = process_webhook.delay(serializer.validated_data)

        return Response(
            {"message": "Webhook received. Processing in background.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return Response(
            {"error": "Internal server error", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@shared_task
def process_webhook(validated_data):
    """
    Asynchronously processes webhook events.

    This function is executed by Celery to handle webhook events in the background.
    Each event type is processed accordingly by calling the appropriate function.

    Parameters:
        validated_data (dict): A dictionary containing the validated webhook data with the following keys:
            - type (str): The event type (e.g., "NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION").
            - timestamp (str): The timestamp of the event.
            - data (dict): The event-specific data.

    Returns:
        dict: A dictionary containing the processing result:
            - "status" (int): HTTP status code representing the result.
            - "data" (dict, optional): Data returned by the event processing (on success).
            - "error" (str, optional): Error message (on failure).
            - "details" (str, optional): Additional error details (on failure).
    """
    try:
        event_type = validated_data['type']
        timestamp = validated_data['timestamp']
        data = validated_data['data']

        handlers = {
            "NEW_CONVERSATION": lambda: create_conversation(data.get('id')),
            "NEW_MESSAGE": lambda: add_message(data, timestamp),
            "CLOSE_CONVERSATION": lambda: close_conversation(data.get('id'))
        }

        # Don't need to check if the event type is in the handlers dictionary,
        # because it's already validated in the serializer
        response_data, response_status = handlers[event_type]()
        return {"status": response_status, "data": response_data}

    except ValidationError as e:
        return {"status":400, "error": str(e)}
    except ObjectDoesNotExist:
        return {"status": 404, "error": "Conversation not found"}
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {"status":500, "error": "Internal server error", "details": str(e)}



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


def conversation_detail_view(request, conversation_id):
    """
    Renders the conversation detail page.

    Parameters:
        request (HttpRequest): The Django HTTP request object.
        conversation_id (str): The unique identifier of the conversation.

    Returns:
        HttpResponse: A rendered HTML page displaying the conversation details..
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'conversation_detail.html', {
        'conversation': conversation
    })