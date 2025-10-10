from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.username', read_only=True)
    recipient = serializers.CharField(source='recipient.username', read_only=True)
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'target_type', 'unread', 'timestamp']
        read_only_fields = ['id', 'actor', 'verb', 'target', 'target_type', 'timestamp']

    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
