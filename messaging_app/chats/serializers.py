from rest_framework import serializers
from .models import CustomUser, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)  # Explicit CharField

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    content = serializers.CharField()  # Explicit CharField

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value

# Conversation Serializer with nested messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'last_message']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None
