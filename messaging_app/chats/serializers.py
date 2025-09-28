from rest_framework import serializers
from .models import Users, Conversation, Message


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        field = ['user_id', 'first_name', 'last_name', 'email', 'password_hash', 'phone_number', 'role', 'created_at', 'display_name']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        field = '__all__'

class ConversationSerializer(serializers.ModelsSerializer):
    class Meta:
        model = Conversation
        field = '__all__'
