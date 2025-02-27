from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('conversations/<uuid:conversation_id>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/<uuid:conversation_id>/view/', views.conversation_detail_view, name='conversation_detail_view'),
]