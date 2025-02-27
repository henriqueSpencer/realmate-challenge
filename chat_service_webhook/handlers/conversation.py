from ..models import Conversation

def create_conversation(conversation_id):
    """
    Creates a new conversation if it does not already exist.

    Parameters:
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        tuple: A dictionary with a success or error message and the corresponding HTTP status code.
    """

    if Conversation.objects.filter(id=conversation_id).exists():
        return {"error": "Conversation already exists"}, 409

    conversation = Conversation.objects.create(id=conversation_id, state="OPEN")
    return {"success": True, "message": "Conversation created", "conversation_id": conversation.id}, 201



def close_conversation(conversation_id):
    """
    Closes an existing conversation.

    Parameters:
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        tuple: A dictionary with a success or error message and the corresponding HTTP status code.
    """
    conversation = Conversation.objects.get(id=conversation_id)
    conversation.state = "CLOSED"
    conversation.save()
    return {"success": True, "message": "Conversation closed", "conversation_id": conversation.id}, 200
