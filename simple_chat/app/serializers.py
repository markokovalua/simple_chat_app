from .models import Thread, Message
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class ReadThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Thread
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = "__all__"

    def validate(self, data):
        participants = self.initial_data.get('participants', [])
        if len(participants) != 2:
            raise serializers.ValidationError("Thread must have 2 participants")
        exists = Thread.objects.filter(participants__in=[participants[0]]).filter(participants__in=[participants[1]])
        if exists:
            raise serializers.ValidationError("The thread for the users already exists")
        return data


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message

        fields = "__all__"
        extra_kwargs = {
            'is_read': {'read_only': True},
            'sender': {'read_only': True}
        }

    def validate(self, data):
        # set sender as authenticated user
        data["sender"] = self.context['request'].user
        return data
