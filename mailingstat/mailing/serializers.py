from rest_framework import serializers

from .models import Mailing
from mailing_service.serializers import MessageSerializer


class MailingSerializer(serializers.ModelSerializer):
    sent = serializers.SerializerMethodField()
    fail = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Mailing
        fields = '__all__'  # Включает все поля модели Campaign + 'sent', 'fail', 'messages'

    def get_sent(self, obj):
        return obj.messages.filter(status='sent').count()

    def get_fail(self, obj):
        return obj.messages.filter(status='failed').count()
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if self.context.get('include_messages', None):
            ret.pop('fail')
            ret.pop('sent')
        else:
            ret.pop('messages')

        return ret