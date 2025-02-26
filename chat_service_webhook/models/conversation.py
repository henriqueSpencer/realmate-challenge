from django.db import models
import uuid


class Conversation(models.Model):
    """
    Model definition for Conversation.
    """
    # On BD OPEN AND CLOSED, ON DJANGO INTERFACE: Open and Closed
    STATES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=10, choices=STATES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.state}"

    class Meta:
        """
        Meta definition for Conversation. - Is metadata about the class.
        https://www.geeksforgeeks.org/meta-class-in-models-django/
        """
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"