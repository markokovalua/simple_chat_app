from .models import Thread
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404


class IsThreadAuthor(BasePermission):
    message = 'Editing/Deleting message is allowed to the participant only.'

    def has_object_permission(self, request, view, obj):
        return obj.participants.all().filter(id=request.user.id)


class IsMessageAuthor(BasePermission):
    message = 'Editing/Deleting message is allowed to the sender only.'

    def has_permission(self, request, view):
        user_id = request.user.id
        thread_id = request.data.get('thread')
        if thread_id:
            thread = get_object_or_404(Thread, pk=thread_id)
            return thread.participants.filter(id=user_id)
        return True

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
