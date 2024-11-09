
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shortuuid import uuid

class AsgiValidateTokenView(APIView):
    """
        get:
            API view for retrieving ticket to connect to websocket .
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        ticket_uuid = uuid()
        user_id = request.user.id
        cache.set(ticket_uuid, user_id, 600)

        return Response({'uuid': ticket_uuid})
