"""General web socket middlewares
"""

from channels.db import database_sync_to_async
from urllib.parse import parse_qsl
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from django.contrib.auth import get_user_model
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        raise Exception(
            'user not found, you may forgot to request a uuid from the server, try auth_for_ws_connection ')


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def auth(self, query_string):
        """
        chick if the queuserry string include the same uuid in the cache
        if yes then fetch the user using the decoded uuid which is the user id
        if raised exception then the uuid is wrong or not sent,
        so close the connection
        """
        query_params = dict(parse_qsl(query_string))
        uuid = query_params.get('uuid')
        user_id = cache.get(uuid)
        # I destroyed uuid for performance and security purposes
        if not cache.delete(uuid):
            raise Exception('uuid not found')
        return await get_user(user_id)

    async def __call__(self, scope, receive, send):
       # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        try:
            query_string = scope['query_string'].decode('utf-8')
            scope['user'] = await self.auth(query_string)
        except Exception as e:
            logger.warning(e)
            return None

        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
