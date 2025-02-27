from ..serializers import MessageSerializer
from ..models import Conversation, Message

def add_message(data, timestamp):
    """
    Adds a new message to an existing conversation.

    Parameters:
        data (dict): A dictionary containing message the details
        timestamp (datetime): The timestamp indicating when the message was sent or received.

    Returns:
        tuple: A dictionary with a success or error message and the corresponding HTTP status code.
    """
    data["timestamp"] = timestamp
    message_serializer = MessageSerializer(data=data)

    # Checking if the conversation exists
    if not Conversation.objects.filter(id=data["conversation_id"]).exists():
        return {"error": "Conversation not exists"}, 409
    # Checking if the conversation is closed before adding a message
    conversation = Conversation.objects.get(id=data["conversation_id"])
    if conversation.state == "CLOSED":
        return {"error": "Cannot add messages to closed conversation"}, 400
    # Checking if the message already exists
    if Message.objects.filter(id=data['id']).exists():
        return {"error": "Message already exists"}, 409

    if message_serializer.is_valid():
        message = Message.objects.create(
            id=data["id"],
            conversation=conversation,
            direction=data["direction"],
            content=data["content"],
            timestamp=data["timestamp"]
        )

        return {"success": True, "message": "Message added", "message_id": message.id}, 201


    return {"error": message_serializer.errors}, 400



