from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    """
    Inline admin configuration for displaying Messages within a Conversation.

    This allows messages to be managed directly from the Conversation admin page.

    Attributes:
        model (Message): The Message model to be displayed inline.
        fields (tuple): Specifies which fields are shown in the inline form.
        readonly_fields (tuple): Fields that are displayed as read-only.
        extra (int): The number of empty message forms displayed by default (0 means none).
    """
    model = Message
    fields = ('id', 'direction', 'content', 'timestamp')
    readonly_fields = ('id', 'created_at')
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Conversations in the Django admin panel.

    This class customizes how Conversations are displayed, searched, and filtered.

    Attributes:
        list_display (tuple): Fields displayed in the conversation list view.
        list_filter (tuple): Fields used for filtering conversations.
        search_fields (tuple): Fields that can be searched.
        readonly_fields (tuple): Fields that cannot be edited in the admin panel.
        inlines (list): Adds the MessageInline class to show related messages inside the conversation admin page.
    """
    list_display = ('id', 'state', 'created_at', 'updated_at')
    list_filter = ('state',)
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Messages in the Django admin panel.

    This class customizes how Messages are displayed, searched, and filtered.

    Attributes:
        list_display (tuple): Fields displayed in the message list view.
        list_filter (tuple): Fields used for filtering messages.
        search_fields (tuple): Fields that can be searched.
        readonly_fields (tuple): Fields that cannot be edited in the admin panel.
    """
    list_display = ('id', 'conversation', 'direction', 'content', 'timestamp')
    list_filter = ('direction', 'conversation')
    search_fields = ('content', 'id', 'conversation__id')
    readonly_fields = ('id', 'created_at')