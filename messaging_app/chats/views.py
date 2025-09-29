from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.contrib.auth import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter, ConversationFilter


User = get_user_model() 

# ViewSet for Conversations
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = ConversationFilter
    search_fields = ['participants_email', 'participants_first_name', 'participants_last_name']
    ordering_fields = ['created_at']


    def get_queryset(self):
        """
        This view should return a list of all conversations for the currently authenticated user.
        """
        return Conversation.objects.filter(participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if not participants_ids or not isinstance(participants_ids, list):
            return Response({'error': 'participants must be a list of user IDs'}, status=status.HTTP_400_BAD_REQUEST)
        participants = User.objects.filter(user_id_in=participants_ids)
        if not participants.exists():
            return Response({'error': 'No valid pariticipants found'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants_set(participants)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


# ViewSet for Messages
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filter.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender_email']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        """
        This view should return a list of all messages from conversartions where the currnet user is a participant
        """
        return Message.objects. filter(conversation__participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        if not conversation_id or not message_body:
            return Response({'error': 'conversation and message body are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            conversation = Conversation.object.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'conversation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user is a participant in the conversation 
        if not conversation.participant.filter(user_id=request.user.user_id).exist():
            return Response({'error': 'You are not a participant in this conversation'}, status=status.HTTP_403_FORBIDDEN)
        
        message = Message.objects.create(sender=request.user, conversation=conversation, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        