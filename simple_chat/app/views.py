from .models import Thread, Message
from .permissions import IsThreadAuthor, IsMessageAuthor
from .serializers import ThreadSerializer, ReadThreadSerializer, MessageSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ThreadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsThreadAuthor]
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        # check if there is already record and return it if exists
        if len(participants) == 2:
            thread = Thread.objects.filter(
                participants__in=[participants[0]], participants__in=[participants[1]]).first()
            if thread:
                return Response(ThreadSerializer(thread).data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # it is needed to write pagination explicitly on list redefinition
        limit = int(request.query_params.get('limit')) if 'limit' in request.query_params else 10
        index = int(request.query_params.get('offset')) if 'offset' in request.query_params else 1
        # show own threads for authenticated user
        threads = self.queryset.filter(participants__in=[request.user.id])
        return Response(ReadThreadSerializer(threads[index - 1: limit], many=True).data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsMessageAuthor]
    queryset = Message.objects.select_related('thread').all()
    serializer_class = MessageSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'thread',
                openapi.IN_QUERY,
                description="set thread id query parameter to show related messages for thread",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'is_read',
                openapi.IN_QUERY,
                description="set show_not_read boolean value query parameter to show not read messages for user",
                type=openapi.TYPE_BOOLEAN,
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        expression = Q(thread__participants__id=request.user.id)
        if "thread" in request.query_params:
            expression = expression & Q(thread__id=request.query_params.get("thread"))
        if "is_read" in request.query_params:
            expression = expression & Q(is_read=request.query_params.get("is_read") != 'false')
        messages = self.queryset.filter(expression)
        limit = int(request.query_params.get('limit')) if 'limit' in request.query_params else 10
        index = int(request.query_params.get('offset')) if 'offset' in request.query_params else 1
        data = MessageSerializer(messages[index - 1: limit], many=True).data
        # set message read
        messages.update(is_read=True)
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'thread',
                openapi.IN_QUERY,
                description="set thread id query parameter to show not read messages count for thread",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    @action(methods=["get"], url_path="is-not-read-count", detail=False)
    def get_unread_message_count(self, request, *args, **kwargs):
        expression = Q(thread__participants__id=request.user.id) & Q(is_read=False)
        if "thread" in request.query_params:
            expression = expression & Q(thread__id=request.query_params.get("thread"))
        return Response({"count":  self.queryset.filter(expression).count()}, status=status.HTTP_200_OK)
