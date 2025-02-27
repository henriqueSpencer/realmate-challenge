from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    fields = ('id', 'direction', 'content', 'timestamp')
    readonly_fields = ('id', 'created_at')
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'created_at', 'updated_at')
    list_filter = ('state',)
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'direction', 'content', 'timestamp')
    list_filter = ('direction', 'conversation')
    search_fields = ('content', 'id', 'conversation__id')
    readonly_fields = ('id', 'created_at')