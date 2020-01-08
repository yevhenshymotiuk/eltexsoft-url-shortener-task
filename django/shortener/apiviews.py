from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import ShortURL
from .serializers import (
    ShortURLSerializer,
    ShortURLStatsRetrieveSerializer,
)
from .utils import client_ip


class IsCreator(BasePermission):
    message = 'Only creator of the url is able to view stats and delete url.'

    def has_permission(self, request, view):
        return client_ip(request) == view.get_object().creator_ip


class ShortURLCreateAPIView(CreateAPIView):
    serializer_class = ShortURLSerializer


class ShortURLStatsRetrieveAPIView(RetrieveAPIView):
    model = ShortURL
    serializer_class = ShortURLStatsRetrieveSerializer
    permission_classes = [IsCreator]

    def get_object(self):
        obj = self.model.objects.get(short_id=self.kwargs.get('short_id'))
        return obj


class ShortURLDestroyAPIView(APIView):
    model = ShortURL
    permission_classes = [IsCreator]

    def get_object(self):
        obj = self.model.objects.get(short_id=self.kwargs.get('short_id'))
        return obj

    def delete(self, *args, **kwargs):
        short_url = self.get_object()
        short_id = short_url.short_id
        short_url.delete()
        return Response({'detail': f'ShortUrl {short_id} was deleted'})
