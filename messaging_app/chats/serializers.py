from rest_framework import serializers
from .models import Users, Conversation, Message


class UsersSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Users
        field = ['user_id', 'first_name', 'last_name', 'email', 'password_hash', 'phone_number', 'role', 'created_at', 'display_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = UsersSerializer(read_only=True)

    class Meta:
        model = Message
        field = '__all__'
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelsSerializer):
    participants = UsersSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        field = '__all__'
        read_only_field = ['conversation_id', 'created_at', 'messages']
    
    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data
    
# Example of ValidationError usage
def validate_role(value):
    allowed_roles = ['guest', 'host', 'admin']
    if value not in allowed_roles:
        raise serializers.ValidationError(f"Role must be one of {allowed_roles}")
    return value