from django.db import models
import uuid
from .conversation import Conversation

class Message(models.Model):
    """
    Model definition for Message.
    """
    # On BD SENT AND RECEIVED, ON DJANGO INTERFACE: Sent and Received
    DIRECTIONS = (
        ('SENT', 'Sent'),
        ('RECEIVED', 'Received'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    direction = models.CharField(max_length=10, choices=DIRECTIONS)
    content = models.TextField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} - {self.direction}"

    class Meta:
        """
        Meta definition for Message.
        https://www.geeksforgeeks.org/meta-class-in-models-django/
        """
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        # Message.objects.all() will return the messages ordered by timestamp in ascending order
        ordering = ['timestamp']