from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.utils.module_loading import import_string
from uuid import uuid4
import logging

# Configure logging
logger = logging.getLogger(__name__)

class AsgiValidateTokenView(APIView):
    """
    API view for retrieving a ticket to connect to websocket.

    get:
        Returns a UUID ticket for websocket connection.
    """
    try:
        # Dynamically load permission classes from settings
        permission_classes = [import_string(perm) for perm in getattr(settings, 'ASGI_VALIDATE_TOKEN_PERMISSION_CLASSES', ['rest_framework.permissions.IsAuthenticated'])]
    except ImportError as e:
        logger.error(f"Error importing permission classes: {e}")
        permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ticket_uuid = uuid4()
        user_id = request.user.id
        try:
            cache.set(str(ticket_uuid), user_id, 600)
            logger.info(f"Ticket created: {ticket_uuid} for user: {user_id}")
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return Response({'error': 'Internal server error'}, status=500)

        return Response({'uuid': ticket_uuid})
