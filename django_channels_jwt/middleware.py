"""General web socket middlewares"""

from channels.db import database_sync_to_async, aclose_old_connections
from urllib.parse import parse_qsl
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.contrib.auth import get_user_model
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except Exception:
        raise Exception(
            "User not found. You may have forgotten to request a ticket from the server "
            "via the auth_for_ws_connection endpoint."
        )


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def auth(self, query_string):
        """
        Check if the query string includes a valid UUID ticket stored in cache.
        If valid, fetch the corresponding user and return it.
        The UUID is deleted from cache immediately for security (one-time use).
        """
        query_params = dict(parse_qsl(query_string))
        uuid = query_params.get("uuid")
        user_id = cache.get(uuid)
        # Destroy UUID immediately for performance and security (one-time use token)
        if not cache.delete(uuid):
            raise Exception("UUID not found or already consumed.")
        return await get_user(user_id)

    async def __call__(self, scope, receive, send):
        # Channels 4.2+ automatically closes old DB connections on connect/disconnect,
        # but we call aclose_old_connections() here as well for safety on older setups.
        await aclose_old_connections()

        try:
            query_string = scope["query_string"].decode("utf-8")
            scope["user"] = await self.auth(query_string)
        except Exception as e:
            logger.warning("WebSocket authentication failed: %s", e)
            return None

        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
